# ResuMatch - Supabase Database Setup Guide

## 🎯 Quick Start for Team Members

This guide will help you set up your local development environment to connect to our shared Supabase database.

---

## 📋 Prerequisites

- Python 3.12.7 installed
- Git repository cloned
- Code editor (VS Code recommended)

---

## 🚀 Step-by-Step Setup

### Step 1: Create Supabase Project (Project Owner Only)

**👤 For the project owner (you):**

1. **Go to Supabase**
   - Visit: https://supabase.com
   - Click "Start your project"

2. **Sign Up / Sign In**
   - Use GitHub, Google, or email

3. **Create New Project**
   - Click "New Project"
   - Organization: Create new or use existing
   - Project Name: `ResuMatch`
   - Database Password: **Create a strong password** (save this!)
   - Region: Choose closest to your team (e.g., `Southeast Asia (Singapore)` or `South Asia (Mumbai)`)
   - Pricing Plan: Free

4. **Wait for Setup**
   - Takes 1-2 minutes to provision database

5. **Get Connection Details**
   - Go to Project Settings → Database
   - Find "Connection string" section
   - Note down these details:
     ```
     Host: db.xxxxxxxxxxxxx.supabase.co
     Database: postgres
     User: postgres
     Password: [your password from step 3]
     Port: 5432
     ```
`
---

### Step 2: Install Python Dependencies

**👥 For all team members:**

```bash
# Navigate to backend directory
cd d:\ResuMatch\Resu_back\backend

# Install required packages
pip install psycopg2-binary python-decouple
```

---

### Step 3: Configure Environment Variables

**👥 For all team members:**

1. **Copy the example file**
   ```bash
   # The .env.example file is already in the repo
   # Copy it to create your own .env file
   cp .env.example .env
   ```

2. **Edit your `.env` file**
   
   Open `d:\ResuMatch\Resu_back\backend\.env` and update with Supabase credentials:

   ```env
   # Database Configuration (Supabase)
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=your_supabase_password_here
   DB_HOST=db.xxxxxxxxxxxxx.supabase.co
   DB_PORT=5432

   # Django Configuration
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

   **⚠️ Important:**
   - Replace `your_supabase_password_here` with the actual password
   - Replace `db.xxxxxxxxxxxxx.supabase.co` with your actual Supabase host
   - All team members use the **same credentials**

---

### Step 4: Update Django Settings

**✅ Already configured in settings.py**

The Django settings have been updated to:
- Read database credentials from `.env` file
- Use PostgreSQL instead of SQLite
- Enable SSL for Supabase connection
- Support environment-based configuration

---

### Step 5: Run Database Migrations

**👥 For all team members:**

```bash
# Navigate to backend directory
cd d:\ResuMatch\Resu_back\backend

# Run migrations to create database tables
python manage.py migrate

# Create a superuser (optional, for admin access)
python manage.py createsuperuser
```

---

### Step 6: Verify Connection

**👥 For all team members:**

```bash
# Test database connection
python manage.py check --database default

# Open Django shell to test
python manage.py shell
```

In the shell, run:
```python
from django.db import connection
print(connection.ensure_connection())
print("✅ Database connected successfully!")
```

---

## 🔐 Security Best Practices

### For Project Owner:

1. **Share Credentials Securely**
   - ❌ Don't share via email or public chat
   - ✅ Use encrypted messaging (Signal, WhatsApp)
   - ✅ Use password manager with sharing (1Password, Bitwarden)
   - ✅ Share in person or via secure channel

2. **Rotate Credentials**
   - Change database password periodically
   - Update team when credentials change

### For All Team Members:

1. **Never Commit `.env` File**
   - Already in `.gitignore`
   - Double-check before pushing code

2. **Keep Credentials Private**
   - Don't share outside the team
   - Don't screenshot or post publicly

3. **Use Strong Passwords**
   - For database
   - For Supabase account

---

## 📊 Supabase Dashboard Features

**Access your database visually:**

1. **Table Editor**
   - View and edit data
   - Create tables manually
   - Run SQL queries

2. **SQL Editor**
   - Write custom queries
   - Create functions and triggers

3. **Database Backups**
   - Automatic daily backups (Free tier: 7 days retention)
   - Manual backups available

4. **Monitoring**
   - Database size
   - Connection count
   - Query performance

---

## 🛠️ Common Issues & Solutions

### Issue 1: "Connection refused"
**Solution:**
- Check if DB_HOST is correct
- Verify internet connection
- Check Supabase project is running

### Issue 2: "Authentication failed"
**Solution:**
- Verify DB_PASSWORD is correct
- Check for extra spaces in .env file
- Ensure using `postgres` as DB_USER

### Issue 3: "SSL required"
**Solution:**
- Already configured in settings.py
- If error persists, check Django settings

### Issue 4: "Too many connections"
**Solution:**
- Free tier: 60 connections max
- Close unused connections
- Check for connection leaks in code

---

## 📝 Team Workflow

### Daily Development:

1. **Pull latest code**
   ```bash
   git pull origin main
   ```

2. **Check for new migrations**
   ```bash
   python manage.py migrate
   ```

3. **Start development**
   ```bash
   python manage.py runserver
   ```

### Creating Database Changes:

1. **Modify models** in Django apps

2. **Create migrations**
   ```bash
   python manage.py makemigrations
   ```

3. **Test locally**
   ```bash
   python manage.py migrate
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Add new model"
   git push
   ```

5. **Notify team** to run migrations

---

## 🎓 Next Steps

After database setup:

1. ✅ Install Django REST Framework
2. ✅ Create Django apps (users, resumes, jobs)
3. ✅ Define models
4. ✅ Create API endpoints
5. ✅ Connect frontend to backend

---

## 📞 Support

**If you encounter issues:**

1. Check this guide first
2. Search Supabase documentation
3. Ask team lead
4. Check Django documentation

---

## 🔗 Useful Links

- **Supabase Dashboard**: https://app.supabase.com
- **Supabase Docs**: https://supabase.com/docs
- **Django Docs**: https://docs.djangoproject.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

**Last Updated**: December 2, 2025  
**Database Provider**: Supabase (Free Tier)  
**Team Size**: 6 developers
