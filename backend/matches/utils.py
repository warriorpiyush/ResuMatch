from django.db.models import Q
from .models import Match
from resumes.models import Resume
from jobs.models import Job

def calculate_match_score(resume, job):
    """
    Calculate match score between a resume and a job.
    Returns a dictionary with detailed scores.
    """
    scores = {
        'overall_score': 0,
        'skill_match_score': 0,
        'experience_match_score': 0,
        'education_match_score': 0,
        'location_match_score': 0,
        'matching_skills': [],
        'missing_skills': [],
        'match_details': {}
    }
    
    # 1. Skill Matching (40%)
    job_skills = set(job.required_skills.values_list('name', flat=True))
    # Normalize skills (lowercase)
    job_skills = {s.lower() for s in job_skills}
    
    resume_skills = set(resume.skills.values_list('name', flat=True))
    # Add skills from parsed text if not in DB
    # (In a real app, we'd extract more from parsed_text)
    resume_skills = {s.lower() for s in resume_skills}
    
    if job_skills:
        matching = job_skills.intersection(resume_skills)
        missing = job_skills.difference(resume_skills)
        
        scores['matching_skills'] = list(matching)
        scores['missing_skills'] = list(missing)
        
        # Jaccard similarity for skills
        # But weighted towards job requirements coverage
        coverage = len(matching) / len(job_skills)
        scores['skill_match_score'] = int(coverage * 100)
    else:
        # If no skills required, give full points (or neutral)
        scores['skill_match_score'] = 100
        
    # 2. Experience Matching (30%)
    # Map levels to numeric values
    levels = {
        'ENTRY': 0,
        'MID': 2,
        'SENIOR': 5,
        'LEAD': 8,
        'EXECUTIVE': 10
    }
    job_level_val = levels.get(job.experience_level, 2)
    
    # Calculate resume experience years
    total_years = 0
    for exp in resume.experiences.all():
        total_years += exp.duration_months / 12
        
    # Simple logic: if years >= required, 100%. Else proportional.
    # Assuming level roughly maps to years: Entry=0-2, Mid=2-5, Senior=5+
    required_years = job_level_val
    if total_years >= required_years:
        scores['experience_match_score'] = 100
    else:
        scores['experience_match_score'] = int((total_years / max(required_years, 1)) * 100)
        
    # 3. Location Matching (15%)
    if job.is_remote:
        scores['location_match_score'] = 100
    else:
        # Check if candidate location matches job location
        # This is very basic string matching
        candidate_loc = ""
        if hasattr(resume.user, 'candidate_profile'):
            candidate_loc = resume.user.candidate_profile.location.lower()
            
        if job.location.lower() in candidate_loc or candidate_loc in job.location.lower():
            scores['location_match_score'] = 100
        else:
            scores['location_match_score'] = 0
            
    # 4. Education Matching (15%)
    # Placeholder: if any education exists, give points
    if resume.education.exists():
        scores['education_match_score'] = 100
    else:
        scores['education_match_score'] = 50
        
    # Calculate Overall Score
    scores['overall_score'] = int(
        (scores['skill_match_score'] * 0.4) +
        (scores['experience_match_score'] * 0.3) +
        (scores['location_match_score'] * 0.15) +
        (scores['education_match_score'] * 0.15)
    )
    
    return scores

def create_or_update_match(resume, job):
    """
    Calculate score and save Match object
    """
    scores = calculate_match_score(resume, job)
    
    match, created = Match.objects.update_or_create(
        resume=resume,
        job=job,
        defaults={
            'overall_score': scores['overall_score'],
            'skill_match_score': scores['skill_match_score'],
            'experience_match_score': scores['experience_match_score'],
            'education_match_score': scores['education_match_score'],
            'location_match_score': scores['location_match_score'],
            'matching_skills': scores['matching_skills'],
            'missing_skills': scores['missing_skills'],
            'match_details': scores['match_details']
        }
    )
    return match
