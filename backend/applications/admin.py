from django.contrib import admin
from .models import Application, ApplicationStatusHistory


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'status', 'match_score', 'applied_at']
    list_filter = ['status', 'applied_at', 'reviewed_at']
    search_fields = ['candidate__username', 'job__title']
    readonly_fields = ['applied_at', 'updated_at', 'reviewed_at']
    date_hierarchy = 'applied_at'


@admin.register(ApplicationStatusHistory)
class ApplicationStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['application', 'old_status', 'new_status', 'changed_by', 'changed_at']
    list_filter = ['old_status', 'new_status', 'changed_at']
    search_fields = ['application__candidate__username', 'application__job__title']
    readonly_fields = ['changed_at']
