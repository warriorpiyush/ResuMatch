from rest_framework import serializers
from .models import Application, ApplicationStatusHistory
from jobs.serializers import JobListSerializer
from resumes.serializers import ResumeListSerializer

class ApplicationStatusHistorySerializer(serializers.ModelSerializer):
    changed_by_name = serializers.CharField(source='changed_by.get_full_name', read_only=True)
    
    class Meta:
        model = ApplicationStatusHistory
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    status_history = ApplicationStatusHistorySerializer(many=True, read_only=True)
    job_details = JobListSerializer(source='job', read_only=True)
    resume_details = ResumeListSerializer(source='resume', read_only=True)
    candidate_name = serializers.CharField(source='candidate.get_full_name', read_only=True)
    candidate_email = serializers.EmailField(source='candidate.email', read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = (
            'candidate', 'status', 'match_score', 'applied_at', 
            'updated_at', 'reviewed_at', 'status_history'
        )

class ApplicationListSerializer(serializers.ModelSerializer):
    """Lighter serializer for lists"""
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.recruiter.recruiter_profile.company_name', read_only=True)
    candidate_name = serializers.CharField(source='candidate.get_full_name', read_only=True)
    
    class Meta:
        model = Application
        fields = (
            'id', 'job_title', 'company_name', 'candidate_name', 
            'status', 'applied_at', 'match_score'
        )
