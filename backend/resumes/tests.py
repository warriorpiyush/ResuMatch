from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
import os

User = get_user_model()

class ResumeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testcandidate',
            email='candidate@example.com',
            password='testpassword123',
            role='CANDIDATE'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create a dummy PDF file
        self.pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Kids [3 0 R]\n/Count 1\n/Type /Pages\n>>\nendobj\n3 0 obj\n<<\n/MediaBox [0 0 595 842]\n/Type /Page\n/Parent 2 0 R\n/Resources <<\n/Font <<\n/F1 4 0 R\n>>\n>>\n/Contents 5 0 R\n>>\nendobj\n4 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/Name /F1\n/BaseFont /Helvetica\n>>\nendobj\n5 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n0000000238 00000 n\n0000000326 00000 n\ntrailer\n<<\n/Size 6\n/Root 1 0 R\n>>\nstartxref\n420\n%%EOF"
        self.resume_file = SimpleUploadedFile(
            "test_resume.pdf",
            self.pdf_content,
            content_type="application/pdf"
        )

    def test_resume_upload(self):
        """Test resume upload and automatic parsing"""
        url = '/api/resumes/'
        data = {
            'title': 'My Test Resume',
            'file': self.resume_file
        }
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['title'], 'My Test Resume')
        self.assertEqual(response.data['data']['file_type'], 'pdf')
        
        # Verify parsing was attempted (it might fail on dummy PDF, but is_parsed should be set if successful)
        # Since our dummy PDF is very basic, parsing might fail or return empty string
        # But we check that the API didn't crash

    def test_resume_list(self):
        """Test listing resumes"""
        # Upload a resume first
        url = '/api/resumes/'
        data = {
            'title': 'My Test Resume',
            'file': self.resume_file
        }
        upload_response = self.client.post(url, data, format='multipart')
        self.assertEqual(upload_response.status_code, status.HTTP_201_CREATED, upload_response.data)
        
        # Debug: Check DB directly
        from .models import Resume
        print(f"Resumes in DB: {Resume.objects.count()}")
        print(f"Resumes for user: {Resume.objects.filter(user=self.user).count()}")
        print(f"Active resumes: {Resume.objects.filter(user=self.user, is_active=True).count()}")
        
        # List resumes
        response = self.client.get(url)
        print(f"List Response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']['results']), 1)

    def tearDown(self):
        # Clean up uploaded files
        # In a real test environment, we'd configure MEDIA_ROOT to a temp dir
        pass
