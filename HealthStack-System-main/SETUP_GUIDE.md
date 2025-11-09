# 🚀 Complete Setup Guide - HealthStack System v2.0

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start (5 minutes)](#quick-start-5-minutes)
3. [Development Setup](#development-setup)
4. [Running Tests](#running-tests)
5. [Common Commands](#common-commands)
6. [Troubleshooting](#troubleshooting)
7. [Next Steps](#next-steps)

---

## Prerequisites

### Required
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)

### Optional (for full features)
- **PostgreSQL 15+** - [Download](https://www.postgresql.org/download/)
- **Redis 7+** - [Download](https://redis.io/download)
- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop)

### Check Installations

```bash
python --version   # Should be 3.11+
git --version      # Any recent version
docker --version   # If using Docker
psql --version     # If using PostgreSQL
redis-cli --version # If using Redis
```

---

## Quick Start (5 minutes)

### For Windows Users

```powershell
# 1. Clone the repository
git clone https://github.com/yourusername/healthstack.git
cd healthstack

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
Copy-Item .env.example .env
# Edit .env file with your settings

# 5. Run migrations
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. Run the server
python manage.py runserver

# Access: http://localhost:8000
# Admin: http://localhost:8000/admin/
```

### For macOS/Linux Users

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/healthstack.git
cd healthstack

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Edit .env file with your settings

# 5. Run migrations
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. Run the server
python manage.py runserver

# Access: http://localhost:8000
# Admin: http://localhost:8000/admin/
```

---

## Development Setup

### 1. Using Makefile (Recommended for Developers)

```bash
# Complete setup in one command
make setup

# This will:
# - Install all dependencies
# - Set up pre-commit hooks
# - Run migrations
# - Collect static files

# Start development server
make run
```

### 2. Manual Setup (Step by Step)

#### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/healthstack.git
cd healthstack
```

#### Step 2: Virtual Environment

```bash
# Create
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Verify activation (you should see (venv) in terminal)
```

#### Step 3: Install Dependencies

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (for testing, linting)
pip install -r requirements-dev.txt
```

#### Step 4: Environment Configuration

```bash
# Copy example file
cp .env.example .env

# Edit with your favorite editor
nano .env
# or
code .env
# or
notepad .env
```

**Minimum Required Settings:**

```env
SECRET_KEY=django-insecure-your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Full Configuration (Optional):**

```env
# Django Core
SECRET_KEY=your-50-character-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL - Optional)
DATABASE_URL=postgresql://healthstack:password@localhost:5432/healthstack

# Redis Cache (Optional)
REDIS_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# SSLCommerz Payment (Optional)
SSLCOMMERZ_STORE_ID=your-store-id
SSLCOMMERZ_STORE_PASSWORD=your-password
SSLCOMMERZ_IS_SANDBOX=True

# Sentry Error Tracking (Optional)
SENTRY_DSN=https://your-sentry-dsn
ENVIRONMENT=development
```

#### Step 5: Database Setup

**Option A: Using SQLite (Default - No setup needed)**

```bash
# Just run migrations
python manage.py migrate
```

**Option B: Using PostgreSQL**

```bash
# 1. Install PostgreSQL
# Download from: https://www.postgresql.org/download/

# 2. Create database
psql -U postgres
CREATE DATABASE healthstack;
CREATE USER healthstack WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE healthstack TO healthstack;
\q

# 3. Update .env
DATABASE_URL=postgresql://healthstack:your-password@localhost:5432/healthstack

# 4. Run migrations
python manage.py migrate
```

#### Step 6: Create Superuser

```bash
python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: admin@healthstack.com
# Password: (enter a strong password)
```

#### Step 7: Load Sample Data (Optional)

```bash
# If you have fixture files
python manage.py loaddata fixtures/sample_hospitals.json
python manage.py loaddata fixtures/sample_doctors.json
```

#### Step 8: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### Step 9: Run Development Server

```bash
python manage.py runserver

# Or run on specific port
python manage.py runserver 8080

# Or make it accessible from network
python manage.py runserver 0.0.0.0:8000
```

---

## Running Tests

### Quick Test Commands

```bash
# Run all tests
make test

# Run with coverage report
make coverage

# Run specific app tests
pytest hospital/tests.py -v
pytest api/tests.py -v

# Run in parallel (faster)
pytest -n auto
```

### Detailed Testing

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests with verbose output
pytest -v

# Run tests with coverage
pytest --cov=. --cov-report=html --cov-report=term

# View coverage report
# Open htmlcov/index.html in browser

# Run specific test class
pytest hospital/tests.py::HospitalModelTest -v

# Run specific test method
pytest hospital/tests.py::HospitalModelTest::test_hospital_creation -v

# Run tests matching pattern
pytest -k "authentication" -v
```

---

## Common Commands

### Development

```bash
# Start server
make run
# or
python manage.py runserver

# Open Django shell
make shell
# or
python manage.py shell

# Create migrations
python manage.py makemigrations

# Apply migrations
make migrate
# or
python manage.py migrate

# Create superuser
make superuser
# or
python manage.py createsuperuser

# Collect static files
make collectstatic
# or
python manage.py collectstatic
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Security check
make security

# Run all quality checks
make quality
```

### Docker

```bash
# Start all services
make docker-up
# or
docker-compose up -d

# View logs
make docker-logs
# or
docker-compose logs -f

# Stop services
make docker-down
# or
docker-compose down

# Run migrations in Docker
make docker-migrate
# or
docker-compose exec web python manage.py migrate

# Access Docker shell
make docker-shell
# or
docker-compose exec web bash
```

### Database

```bash
# Create database backup
make db-backup

# Restore from backup
make db-restore

# Reset database (careful!)
python manage.py flush

# Show migrations
python manage.py showmigrations
```

---

## Troubleshooting

### Issue: "No module named 'django'"

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "django.core.exceptions.ImproperlyConfigured: Set the SECRET_KEY"

**Solution:**
```bash
# Create .env file
cp .env.example .env

# Add SECRET_KEY
echo "SECRET_KEY=django-insecure-$(openssl rand -base64 50)" >> .env
```

### Issue: "Port 8000 is already in use"

**Solution:**
```bash
# Find and kill process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Or run on different port
python manage.py runserver 8080
```

### Issue: Database connection error

**Solution:**
```bash
# Check if PostgreSQL is running
# Windows:
pg_isready

# macOS/Linux:
sudo systemctl status postgresql

# Verify DATABASE_URL in .env
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL
```

### Issue: Redis connection error

**Solution:**
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# Start Redis
# Windows: redis-server
# macOS: brew services start redis
# Linux: sudo systemctl start redis
```

### Issue: Static files not loading

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check settings
python manage.py diffsettings | grep STATIC

# In development, ensure DEBUG=True
```

### Issue: Tests failing

**Solution:**
```bash
# Update test database
pytest --create-db

# Clear pytest cache
pytest --cache-clear

# Run with verbose output
pytest -vvs
```

---

## Next Steps

### After Setup

1. **Explore Admin Panel**
   - Go to http://localhost:8000/admin/
   - Login with superuser credentials
   - Add hospitals, doctors, patients

2. **Test User Flows**
   - Register as patient
   - Browse hospitals
   - Book appointment
   - Test chat feature

3. **API Testing**
   - Access API at http://localhost:8000/api/
   - Get JWT token: POST /api/users/token/
   - Test endpoints with Postman or curl

4. **Review Documentation**
   - Read [ARCHITECTURE.md](ARCHITECTURE.md)
   - Check [DEPLOYMENT.md](DEPLOYMENT.md)
   - Review [IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md)

### For Development

```bash
# Install pre-commit hooks
pre-commit install

# Before committing
make quality  # Run all checks

# Create feature branch
git checkout -b feature/your-feature

# Make changes and test
make test

# Commit
git add .
git commit -m "Add feature: description"

# Push
git push origin feature/your-feature
```

### For Production

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Production settings configuration
- Docker deployment
- Kubernetes deployment
- Cloud deployment (AWS, GCP, Azure)
- Security checklist

---

## 🎉 Success!

If you've reached here, your HealthStack system should be running!

- **Web**: http://localhost:8000
- **Admin**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/

### Default Admin Credentials (if you set them up)
- **Username**: `admin_skismail`
- **Password**: `Ismail@5767`

### Quick Access URLs
- Patient Dashboard: http://localhost:8000/patient-dashboard/
- Doctor Dashboard: http://localhost:8000/doctor-dashboard/
- Hospital Admin: http://localhost:8000/hospital_admin/
- Pharmacy: http://localhost:8000/pharmacy/
- API Docs: http://localhost:8000/api/

---

## 📞 Need Help?

- **Documentation**: Check the docs folder
- **Issues**: https://github.com/yourusername/healthstack/issues
- **Discussions**: https://github.com/yourusername/healthstack/discussions

---

**Happy Coding! 🚀**

*Version: 2.0.0*  
*Last Updated: November 2024*
