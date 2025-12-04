from rest_framework import serializers
from .models import Job, JobSkill, JobCategory
from users.serializers import UserSerializer

class JobSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSkill
        fields = '__all__'
        read_only_fields = ('job',)

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    required_skills = JobSkillSerializer(many=True, read_only=True)
    recruiter = UserSerializer(read_only=True)
    categories = JobCategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = (
            'recruiter', 'views_count', 'applications_count', 
            'created_at', 'updated_at'
        )

class JobListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views"""
    recruiter_name = serializers.CharField(source='recruiter.get_full_name', read_only=True)
    company_name = serializers.CharField(source='recruiter.recruiter_profile.company_name', read_only=True)
    
    class Meta:
        model = Job
        fields = (
            'id', 'title', 'company_name', 'location', 'job_type', 
            'experience_level', 'salary_min', 'salary_max', 'salary_currency',
            'is_remote', 'posted_date', 'recruiter_name'
        )
