from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'CANDIDATE'
        }

    def test_registration(self):
        """Test user registration with standard response format"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['username'], self.user_data['username'])
        self.assertEqual(response.data['data']['email'], self.user_data['email'])
        self.assertEqual(response.data['data']['role'], self.user_data['role'])
        
        # Verify user was created in DB
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())
        
        # Verify profile was created
        user = User.objects.get(email=self.user_data['email'])
        self.assertTrue(hasattr(user, 'candidate_profile'))

    def test_login(self):
        """Test login returns JWT token"""
        # Register first
        self.client.post(self.register_url, self.user_data)
        
        # Login
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_details(self):
        """Test retrieving user details with token"""
        # Register and login
        self.client.post(self.register_url, self.user_data)
        login_response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        token = login_response.data['access']
        
        # Get details
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/users/me/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['username'], self.user_data['username'])
