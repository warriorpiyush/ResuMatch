from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Job

User = get_user_model()

class JobTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create recruiter
        self.recruiter = User.objects.create_user(
            username='recruiter',
            email='recruiter@example.com',
            password='testpassword123',
            role='RECRUITER'
        )
        
        # Create candidate
        self.candidate = User.objects.create_user(
            username='candidate',
            email='candidate@example.com',
            password='testpassword123',
            role='CANDIDATE'
        )
        
        self.job_data = {
            'title': 'Senior Python Developer',
            'description': 'We are looking for an expert.',
            'requirements': 'Python, Django, React',
            'location': 'Remote',
            'job_type': 'FULL_TIME',
            'experience_level': 'SENIOR',
            'salary_min': 100000,
            'salary_max': 150000,
            'is_remote': True
        }

    def test_create_job_recruiter(self):
        """Test recruiter can create a job"""
        self.client.force_authenticate(user=self.recruiter)
        url = '/api/jobs/'
        response = self.client.post(url, self.job_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['title'], self.job_data['title'])
        self.assertEqual(response.data['data']['status'], 'ACTIVE')

    def test_create_job_candidate(self):
        """Test candidate cannot create a job"""
        self.client.force_authenticate(user=self.candidate)
        url = '/api/jobs/'
        response = self.client.post(url, self.job_data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_jobs(self):
        """Test listing active jobs"""
        # Create a job first
        self.client.force_authenticate(user=self.recruiter)
        self.client.post('/api/jobs/', self.job_data)
        
        # List jobs as candidate
        self.client.force_authenticate(user=self.candidate)
        response = self.client.get('/api/jobs/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']['results']), 1)

    def test_filter_jobs(self):
        """Test filtering jobs"""
        self.client.force_authenticate(user=self.recruiter)
        
        # Create Remote job
        self.client.post('/api/jobs/', self.job_data)
        
        # Create On-site job
        onsite_data = self.job_data.copy()
        onsite_data['title'] = 'Onsite Developer'
        onsite_data['is_remote'] = False
        self.client.post('/api/jobs/', onsite_data)
        
        # Filter for Remote
        response = self.client.get('/api/jobs/?is_remote=true')
        self.assertEqual(len(response.data['data']['results']), 1)
        self.assertEqual(response.data['data']['results'][0]['title'], 'Senior Python Developer')
