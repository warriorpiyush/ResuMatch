# ResuMatch Backend Overview

## 🚀 Project Status
- **Framework**: Django 5.2.7 + Django REST Framework 3.15.2
- **Database**: PostgreSQL (Supabase)
- **Authentication**: JWT (SimpleJWT)
- **Documentation**: Swagger UI (`/swagger/`)

## 📦 Apps & Features

### 1. Users (`users`)
- **Models**: `User` (Custom), `CandidateProfile`, `RecruiterProfile`
- **Roles**: Candidate, Recruiter, Admin
- **Features**: Registration, Login, Profile Management

### 2. Resumes (`resumes`)
- **Models**: `Resume`, `Skill`, `Experience`, `Education`
- **Features**: 
  - PDF/DOCX Upload & Parsing
  - Automatic Skill Extraction
  - AI Scoring (Basic implementation)

### 3. Jobs (`jobs`)
- **Models**: `Job`, `JobSkill`
- **Features**: 
  - Job Posting (Recruiters)
  - Job Search & Filtering
  - Application Tracking

### 4. Matches (`matches`)
- **Models**: `Match`
- **Features**: 
  - Intelligent Matching Algorithm (Skills, Experience, Location)
  - Match Score Calculation (0-100%)

### 5. Applications (`applications`)
- **Models**: `Application`, `ApplicationStatusHistory`
- **Features**: 
  - Job Application Workflow
  - Status Tracking (Pending -> Reviewed -> Interview -> Offer)

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Get JWT tokens
- `POST /api/auth/refresh/` - Refresh access token

### Users
- `GET /api/users/me/` - Get current user details
- `GET /api/users/me/candidate-profile/` - Get/Update candidate profile
- `GET /api/users/me/recruiter-profile/` - Get/Update recruiter profile

### Resumes
- `GET /api/resumes/` - List my resumes
- `POST /api/resumes/` - Upload new resume
- `GET /api/resumes/{id}/` - Get resume details
- `GET /api/resumes/{id}/analysis/` - Get analysis scores

### Jobs
- `GET /api/jobs/` - List active jobs (Filterable)
- `POST /api/jobs/` - Post new job (Recruiter only)
- `GET /api/jobs/my-jobs/` - List my posted jobs (Recruiter only)

### Matches
- `GET /api/matches/` - Get my matches
- `POST /api/matches/calculate/` - Trigger match calculation

### Applications
- `POST /api/applications/` - Apply for a job
- `GET /api/applications/` - List my applications
- `PATCH /api/applications/{id}/` - Update status (Recruiter only)

## 🛠️ Development Tools

### Run Tests
```bash
python manage.py test users jobs matches applications
```

### Reset Database
```bash
python manage.py reset_database
```

### Access Admin
- URL: `/admin/`
- Create Superuser: `python manage.py createsuperuser`
