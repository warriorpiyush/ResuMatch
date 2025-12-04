import os
import PyPDF2
import docx
from django.conf import settings

def parse_resume(file_path, file_type):
    """
    Extract text from resume file
    """
    text = ""
    try:
        if file_type == 'pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        
        elif file_type == 'docx':
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
                
        return text.strip()
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return ""

def analyze_resume(text):
    """
    Basic analysis of resume text
    Returns a dictionary of scores and extracted info
    """
    # This is a placeholder for more advanced AI analysis
    # In a real app, you might use OpenAI or a specialized NLP library
    
    scores = {
        'overall_score': 0,
        'keyword_score': 0,
        'format_score': 0,
        'experience_score': 0,
        'achievement_score': 0
    }
    
    if not text:
        return scores
        
    # Basic scoring logic (mock)
    word_count = len(text.split())
    
    # Length score
    if 200 <= word_count <= 1000:
        scores['format_score'] = 80
    else:
        scores['format_score'] = 50
        
    # Keyword score (mock)
    keywords = ['python', 'django', 'javascript', 'react', 'sql', 'git', 'aws', 'docker']
    found_keywords = [k for k in keywords if k.lower() in text.lower()]
    scores['keyword_score'] = min(len(found_keywords) * 10, 100)
    
    # Experience score (mock - looking for years)
    import re
    years = re.findall(r'(\d+)\+?\s*years?', text.lower())
    if years:
        max_years = max([int(y) for y in years])
        scores['experience_score'] = min(max_years * 10, 100)
    else:
        scores['experience_score'] = 40
        
    # Achievement score (mock - looking for action verbs)
    action_verbs = ['achieved', 'developed', 'created', 'managed', 'led', 'improved', 'increased']
    found_verbs = [v for v in action_verbs if v.lower() in text.lower()]
    scores['achievement_score'] = min(len(found_verbs) * 15, 100)
    
    # Overall score
    scores['overall_score'] = int(
        (scores['keyword_score'] * 0.4) + 
        (scores['experience_score'] * 0.3) + 
        (scores['format_score'] * 0.15) + 
        (scores['achievement_score'] * 0.15)
    )
    
    return scores
