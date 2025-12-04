from django.contrib import admin
from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['resume', 'job', 'overall_score', 'match_quality', 'created_at']
    list_filter = ['overall_score', 'is_viewed_by_candidate', 'is_viewed_by_recruiter', 'created_at']
    search_fields = ['resume__title', 'job__title']
    readonly_fields = ['created_at', 'updated_at', 'match_quality']
    
    def match_quality(self, obj):
        return obj.match_quality
    match_quality.short_description = 'Quality'
