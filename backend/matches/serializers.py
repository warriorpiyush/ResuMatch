from rest_framework import serializers
from .models import Match
from resumes.serializers import ResumeListSerializer
from jobs.serializers import JobListSerializer

class MatchSerializer(serializers.ModelSerializer):
    resume = ResumeListSerializer(read_only=True)
    job = JobListSerializer(read_only=True)
    
    class Meta:
        model = Match
        fields = '__all__'
        read_only_fields = (
            'overall_score', 'skill_match_score', 'experience_match_score',
            'education_match_score', 'location_match_score',
            'matching_skills', 'missing_skills', 'match_details',
            'created_at', 'updated_at'
        )

class MatchListSerializer(serializers.ModelSerializer):
    """Lighter serializer for lists"""
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.recruiter.recruiter_profile.company_name', read_only=True)
    candidate_name = serializers.CharField(source='resume.user.get_full_name', read_only=True)
    
    class Meta:
        model = Match
        fields = (
            'id', 'job_title', 'company_name', 'candidate_name', 
            'overall_score', 'match_quality', 'created_at',
            'is_viewed_by_candidate', 'is_viewed_by_recruiter'
        )
