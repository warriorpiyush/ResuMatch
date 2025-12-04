from django.contrib import admin
from .models import Job, JobSkill, JobCategory


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'recruiter', 'status', 'job_type', 'views_count', 'applications_count', 'created_at']
    list_filter = ['status', 'job_type', 'experience_level', 'is_remote', 'created_at']
    search_fields = ['title', 'description', 'recruiter__username']
    readonly_fields = ['views_count', 'applications_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(JobSkill)
class JobSkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'job', 'is_required', 'proficiency_level']
    list_filter = ['is_required', 'proficiency_level']
    search_fields = ['name', 'job__title']


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
