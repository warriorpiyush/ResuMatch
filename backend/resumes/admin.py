from django.contrib import admin
from .models import Resume, Skill, Experience, Education, Certification


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'overall_score', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_parsed', 'created_at']
    search_fields = ['title', 'user__username', 'parsed_text']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'resume', 'proficiency', 'is_primary']
    list_filter = ['proficiency', 'is_primary']
    search_fields = ['name', 'resume__title']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'resume', 'start_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['position', 'company', 'resume__title']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'field_of_study', 'resume', 'start_date']
    list_filter = ['is_current', 'start_date']
    search_fields = ['degree', 'institution', 'field_of_study']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuing_organization', 'resume', 'issue_date']
    list_filter = ['issue_date']
    search_fields = ['name', 'issuing_organization']
