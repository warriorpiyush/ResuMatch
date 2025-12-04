from rest_framework import serializers
from .models import Resume, Skill, Experience, Education, Certification

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ('resume',)

class ExperienceSerializer(serializers.ModelSerializer):
    duration_months = serializers.ReadOnlyField()
    
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ('resume',)

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('resume',)

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'
        read_only_fields = ('resume',)

class ResumeSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = (
            'user', 'parsed_text', 'overall_score', 'keyword_score', 
            'format_score', 'experience_score', 'achievement_score',
            'file_size', 'is_parsed'
        )

class ResumeListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views"""
    class Meta:
        model = Resume
        fields = ('id', 'title', 'created_at', 'is_active', 'overall_score')
