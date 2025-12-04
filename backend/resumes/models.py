from django.db import models
from users.models import User


class Resume(models.Model):
    """Main resume model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='resumes/')
    file_type = models.CharField(max_length=10)  # pdf, docx
    file_size = models.IntegerField(default=0)  # in bytes
    parsed_text = models.TextField(blank=True)
    
    # Analysis scores
    overall_score = models.IntegerField(default=0)
    keyword_score = models.IntegerField(default=0)
    format_score = models.IntegerField(default=0)
    experience_score = models.IntegerField(default=0)
    achievement_score = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    is_parsed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'resumes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Skill(models.Model):
    """Skills extracted from resume"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50, blank=True)  # Beginner, Intermediate, Expert
    years_of_experience = models.IntegerField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)  # Mark primary skills
    
    class Meta:
        db_table = 'skills'
        ordering = ['-is_primary', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.resume.title})"


class Experience(models.Model):
    """Work experience"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    achievements = models.JSONField(default=list, blank=True)  # List of achievements
    
    class Meta:
        db_table = 'experiences'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
    @property
    def duration_months(self):
        """Calculate duration in months"""
        from datetime import date
        end = self.end_date or date.today()
        months = (end.year - self.start_date.year) * 12 + (end.month - self.start_date.month)
        return max(months, 0)


class Education(models.Model):
    """Educational background"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    is_current = models.BooleanField(default=False)
    achievements = models.TextField(blank=True)
    
    class Meta:
        db_table = 'education'
        ordering = ['-start_date']
        verbose_name_plural = 'Education'
    
    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.institution}"


class Certification(models.Model):
    """Professional certifications"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    
    class Meta:
        db_table = 'certifications'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"
