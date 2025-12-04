# ResuMatch Backend

Django backend for the ResuMatch AI-powered resume and job matching platform.

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL (via Supabase)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ResuMatch/Resu_back/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your Supabase credentials
   # Get credentials from project owner or Supabase dashboard
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

   Server will start at: http://localhost:8000

## 📁 Project Structure

```
backend/
├── backend/           # Django project settings
│   ├── settings.py   # Configuration
│   ├── urls.py       # URL routing
│   └── wsgi.py       # WSGI config
├── manage.py         # Django CLI
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variables template
└── SETUP_INSTRUCTIONS.md  # Detailed setup guide
```

## 🗄️ Database

- **Provider**: Supabase (PostgreSQL)
- **Type**: Shared development database
- **Access**: All team members use same credentials
- **SSL**: Required (automatically configured)

## 🔐 Environment Variables

Required variables in `.env`:

```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**⚠️ Never commit `.env` file to Git!**

## 📚 Documentation

- [Detailed Setup Instructions](SETUP_INSTRUCTIONS.md)
- [Django Documentation](https://docs.djangoproject.com)
- [Supabase Documentation](https://supabase.com/docs)

## 🛠️ Development Workflow

1. Pull latest changes: `git pull origin main`
2. Check for new migrations: `python manage.py migrate`
3. Make your changes
4. Create migrations (if models changed): `python manage.py makemigrations`
5. Test locally: `python manage.py runserver`
6. Commit and push: `git add . && git commit -m "message" && git push`

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
```

## 📦 Dependencies

- **Django 5.2.7** - Web framework
- **psycopg2-binary** - PostgreSQL adapter
- **python-decouple** - Environment variables
- **djangorestframework** - API development
- **django-cors-headers** - CORS support
- **djangorestframework-simplejwt** - JWT authentication

See `requirements.txt` for complete list.

## 🤝 Team Collaboration

- **Team Size**: 6 developers
- **Database**: Shared Supabase instance
- **Workflow**: Git-based collaboration
- **Communication**: Coordinate migrations and schema changes

## 🐛 Troubleshooting

### Database connection issues
- Verify `.env` credentials are correct
- Check internet connection
- Ensure Supabase project is active

### Migration conflicts
- Pull latest code first
- Run `python manage.py migrate`
- If conflicts persist, contact team lead

### Import errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

## 📞 Support

For issues or questions:
1. Check `SETUP_INSTRUCTIONS.md`
2. Review Django/Supabase documentation
3. Ask team lead
4. Create GitHub issue

## 📝 License

[Your License Here]

## 👥 Team

- Project Lead: [Your Name]
- Team Members: 6 developers

---

**Last Updated**: December 2, 2025
