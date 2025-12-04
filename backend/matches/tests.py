from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Match
from .utils import calculate_match_score
from jobs.models import Job, JobSkill
from resumes.models import Resume, Skill, Experience

User = get_user_model()

class MatchTests(TestCase):
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
            requirements='Python, Django',
            location='Remote',
            status='ACTIVE',
            experience_level='MID'
        )
        JobSkill.objects.create(job=self.job, name='Python')
        JobSkill.objects.create(job=self.job, name='Django')
        
        # Create Resume
        self.resume = Resume.objects.create(
            user=self.candidate,
            title='My Resume',
            file_type='pdf',
            is_active=True
        )
        Skill.objects.create(resume=self.resume, name='Python')
        Skill.objects.create(resume=self.resume, name='Django')
        Experience.objects.create(
            resume=self.resume,
            company='Tech Corp',
            position='Dev',
            start_date='2020-01-01',
            end_date='2023-01-01' # 3 years
        )

    def test_match_calculation_logic(self):
        """Test the scoring algorithm directly"""
        scores = calculate_match_score(self.resume, self.job)
        
        # Skills: 2/2 match = 100%
        self.assertEqual(scores['skill_match_score'], 100)
        self.assertEqual(len(scores['matching_skills']), 2)
        
        # Experience: 3 years vs Mid (2 years) = 100%
        self.assertEqual(scores['experience_match_score'], 100)
        
        # Location: Remote = 100%
        self.assertEqual(scores['location_match_score'], 100)
        
        # Overall should be high
        self.assertTrue(scores['overall_score'] > 90)

    def test_calculate_matches_api(self):
        """Test triggering match calculation via API"""
        self.client.force_authenticate(user=self.candidate)
        
        # Trigger calculation
        response = self.client.post('/api/matches/calculate/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        # Verify match created
        match = Match.objects.get(resume=self.resume, job=self.job)
        self.assertTrue(match.overall_score > 0)

    def test_list_matches(self):
        """Test listing matches"""
        # Create match first
        from .utils import create_or_update_match
        create_or_update_match(self.resume, self.job)
        
        self.client.force_authenticate(user=self.candidate)
        response = self.client.get('/api/matches/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']['results']), 1)
        self.assertEqual(response.data['data']['results'][0]['job_title'], 'Python Dev')
