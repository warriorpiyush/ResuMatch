from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Application
from jobs.models import Job
from resumes.models import Resume

User = get_user_model()

class ApplicationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create users
        self.recruiter = User.objects.create_user(username='recruiter', role='RECRUITER')
        self.candidate = User.objects.create_user(username='candidate', role='CANDIDATE')
        
        # Create Job
        self.job = Job.objects.create(
            recruiter=self.recruiter,
            title='Python Dev',
            description='Need Python expert',
            requirements='Python',
            location='Remote',
            status='ACTIVE'
        )
        
        # Create Resume
        self.resume = Resume.objects.create(
            user=self.candidate,
            title='My Resume',
            file_type='pdf',
            is_active=True
        )

    def test_apply_job(self):
        """Test candidate applying for a job"""
        self.client.force_authenticate(user=self.candidate)
        url = '/api/applications/'
        data = {
            'job': self.job.id,
            'resume': self.resume.id
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['status'], 'PENDING')
        
        # Verify DB
        self.assertTrue(Application.objects.filter(candidate=self.candidate, job=self.job).exists())

    def test_list_applications_candidate(self):
        """Test candidate listing their applications"""
        # Apply first
        Application.objects.create(candidate=self.candidate, job=self.job, resume=self.resume)
        
        self.client.force_authenticate(user=self.candidate)
        response = self.client.get('/api/applications/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['results']), 1)

    def test_update_status_recruiter(self):
        """Test recruiter updating application status"""
        app = Application.objects.create(candidate=self.candidate, job=self.job, resume=self.resume)
        
        self.client.force_authenticate(user=self.recruiter)
        url = f'/api/applications/{app.id}/'
        data = {
            'status': 'REVIEWED',
            'recruiter_notes': 'Looks good'
        }
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['status'], 'REVIEWED')
        
        # Verify history
        app.refresh_from_db()
        self.assertEqual(app.status, 'REVIEWED')
        self.assertTrue(app.status_history.exists())

    def test_withdraw_application(self):
        """Test candidate withdrawing application"""
        app = Application.objects.create(candidate=self.candidate, job=self.job, resume=self.resume)
        
        self.client.force_authenticate(user=self.candidate)
        url = f'/api/applications/{app.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        app.refresh_from_db()
        self.assertEqual(app.status, 'WITHDRAWN')
