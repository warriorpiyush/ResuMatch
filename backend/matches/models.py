from django.db import models
from resumes.models import Resume
from jobs.models import Job


class Match(models.Model):
    """Job-Resume match with score"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='matches')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='matches')
    
    # Overall match score (0-100)
    overall_score = models.IntegerField()
    
    # Component scores
    skill_match_score = models.IntegerField(default=0)
    experience_match_score = models.IntegerField(default=0)
    education_match_score = models.IntegerField(default=0)
    location_match_score = models.IntegerField(default=0)
    
    # Match details (JSON)
    matching_skills = models.JSONField(default=list, blank=True)  # List of matching skills
    missing_skills = models.JSONField(default=list, blank=True)   # List of missing skills
    match_details = models.JSONField(default=dict, blank=True)    # Additional match info
    
    # Status
    is_viewed_by_candidate = models.BooleanField(default=False)
    is_viewed_by_recruiter = models.BooleanField(default=False)
    is_favorited_by_candidate = models.BooleanField(default=False)
    is_favorited_by_recruiter = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'matches'
        ordering = ['-overall_score', '-created_at']
        unique_together = ['resume', 'job']
        indexes = [
            models.Index(fields=['-overall_score', '-created_at']),
            models.Index(fields=['resume', '-overall_score']),
            models.Index(fields=['job', '-overall_score']),
        ]
    
    def __str__(self):
        return f"Match: {self.resume.title} <-> {self.job.title} ({self.overall_score}%)"
    
    @property
    def match_percentage(self):
        """Return overall score as percentage"""
        return self.overall_score
    
    @property
    def match_quality(self):
        """Return match quality label"""
        if self.overall_score >= 90:
            return "Excellent"
        elif self.overall_score >= 75:
            return "Good"
        elif self.overall_score >= 60:
            return "Fair"
        else:
            return "Poor"
