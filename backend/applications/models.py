from django.db import models
from users.models import User
from jobs.models import Job
from resumes.models import Resume


class Application(models.Model):
    """Job application tracking"""
    
    class ApplicationStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Review'
        REVIEWED = 'REVIEWED', 'Reviewed'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        INTERVIEW_SCHEDULED = 'INTERVIEW_SCHEDULED', 'Interview Scheduled'
        INTERVIEW_COMPLETED = 'INTERVIEW_COMPLETED', 'Interview Completed'
        OFFERED = 'OFFERED', 'Offer Extended'
        ACCEPTED = 'ACCEPTED', 'Offer Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        WITHDRAWN = 'WITHDRAWN', 'Withdrawn'
    
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='applications')
    
    cover_letter = models.TextField(blank=True)
    status = models.CharField(
        max_length=30,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING
    )
    
    # Match score at time of application
    match_score = models.IntegerField(null=True, blank=True)
    
    # Recruiter notes
    recruiter_notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Interview details
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_notes = models.TextField(blank=True)
    
    # Offer details
    offer_salary = models.IntegerField(null=True, blank=True)
    offer_details = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'applications'
        ordering = ['-applied_at']
        unique_together = ['candidate', 'job']
        indexes = [
            models.Index(fields=['candidate', '-applied_at']),
            models.Index(fields=['job', 'status', '-applied_at']),
            models.Index(fields=['status', '-applied_at']),
        ]
    
    def __str__(self):
        return f"{self.candidate.username} -> {self.job.title} ({self.get_status_display()})"
    
    def update_status(self, new_status, notes=''):
        """Update application status with timestamp"""
        from django.utils import timezone
        self.status = new_status
        if notes:
            self.recruiter_notes = notes
        if new_status == self.ApplicationStatus.REVIEWED and not self.reviewed_at:
            self.reviewed_at = timezone.now()
        self.save()


class ApplicationStatusHistory(models.Model):
    """Track status changes for applications"""
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=30)
    new_status = models.CharField(max_length=30)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'application_status_history'
        ordering = ['-changed_at']
        verbose_name_plural = 'Application Status Histories'
    
    def __str__(self):
        return f"{self.application.id}: {self.old_status} -> {self.new_status}"
