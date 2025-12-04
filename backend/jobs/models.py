from django.db import models
from users.models import User


class Job(models.Model):
    """Job posting model"""
    
    class JobType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', 'Full-time'
        PART_TIME = 'PART_TIME', 'Part-time'
        CONTRACT = 'CONTRACT', 'Contract'
        TEMPORARY = 'TEMPORARY', 'Temporary'
        INTERNSHIP = 'INTERNSHIP', 'Internship'
    
    class JobStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        CLOSED = 'CLOSED', 'Closed'
        DRAFT = 'DRAFT', 'Draft'
        PAUSED = 'PAUSED', 'Paused'
    
    class ExperienceLevel(models.TextChoices):
        ENTRY = 'ENTRY', 'Entry Level'
        MID = 'MID', 'Mid Level'
        SENIOR = 'SENIOR', 'Senior Level'
        LEAD = 'LEAD', 'Lead/Principal'
        EXECUTIVE = 'EXECUTIVE', 'Executive'
    
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    
    location = models.CharField(max_length=200)
    is_remote = models.BooleanField(default=False)
    
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='USD')
    
    job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)
    experience_level = models.CharField(max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.MID)
    status = models.CharField(max_length=20, choices=JobStatus.choices, default=JobStatus.DRAFT)
    
    # Analytics
    views_count = models.IntegerField(default=0)
    applications_count = models.IntegerField(default=0)
    
    # Dates
    posted_date = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jobs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['recruiter', 'status']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recruiter.username}"
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def increment_applications(self):
        """Increment application count"""
        self.applications_count += 1
        self.save(update_fields=['applications_count'])


class JobSkill(models.Model):
    """Required skills for job"""
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='required_skills')
    name = models.CharField(max_length=100)
    is_required = models.BooleanField(default=True)
    proficiency_level = models.CharField(max_length=50, blank=True)  # Beginner, Intermediate, Expert
    years_required = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'job_skills'
        ordering = ['-is_required', 'name']
    
    def __str__(self):
        return f"{self.name} ({'Required' if self.is_required else 'Preferred'})"


class JobCategory(models.Model):
    """Job categories/industries"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    jobs = models.ManyToManyField(Job, related_name='categories', blank=True)
    
    class Meta:
        db_table = 'job_categories'
        verbose_name_plural = 'Job Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
