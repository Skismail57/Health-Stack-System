# 🏥 HealthStack — Comprehensive Healthcare Management System (Full README)

https://img.shields.io/badge/Django-4.2.16-green.svg
https://img.shields.io/badge/Django%2520REST%2520Framework-3.14-blue.svg
https://img.shields.io/badge/Python-3.8%252B-yellow.svg
https://img.shields.io/badge/PostgreSQL-Supported-blue.svg
https://img.shields.io/badge/Redis-Optional-red.svg

📋 Table of Contents
- Overview
- Features
- Project Structure
- Tech Stack
- Installation
- Configuration
- Usage
- API Documentation
- Screenshots
- Deployment
- Contributing
- License

🎯 Overview

HealthStack is a comprehensive, modular Django-powered healthcare platform that unifies patients, doctors, hospitals, and pharmacies into a seamless digital ecosystem. The system provides end-to-end healthcare management with real-time communication, AI-powered symptom checking, and secure payment processing.

🏗️ Architecture
- Modular Design: Separate apps for each functional domain
- RESTful APIs: JWT-secured endpoints with auto-generated documentation
- Real-time Features: WebSocket-based chat system
- Production Ready: Configurable for SQLite (dev) or PostgreSQL (production)

### Core Apps
- Hospital portal: `hospital/` — hospital homepage, profiles, search, bookings, dashboards
- Doctor portal: `doctor/` — authentication, scheduling, consultations, prescriptions, reports
- Pharmacy: `pharmacy/` — catalog, cart, orders, prescription upload, checkout
- Chat: `ChatApp/` — real‑time messaging (Django Channels/WebSockets)
- AI: `ai/` — symptom checker and doctor recommendations
- API: `api/` — DRF endpoints, JWT auth, auto docs (drf‑spectacular)
- Payments: `sslcommerz/` — payment request, success/fail/cancel flows

✨ Features

👥 Patient Portal
- User Management: Registration, login, and profile management
- Smart Search: Find doctors by specialization, location, and ratings
- Appointment System: Real-time availability checking and booking
- Medical Records: Digital prescriptions and health history
- E-Pharmacy: Medicine orders with prescription upload
- Communication: Real-time chat with healthcare providers
- Payment Tracking: History and notification system

🩺 Doctor Portal
- Professional Profile: Complete profile management with credentials
- Schedule Management: Availability and appointment scheduling
- Clinical Tools: Digital prescriptions and medical reports
- Patient Management: History tracking and timeline views
- Analytics: Earnings overview and performance insights

🏥 Hospital Admin
- Hospital Profile: Department, facility, and service management
- Monitoring: Real-time appointment tracking and patient analytics
- Staff Management: Doctor approval and performance monitoring
- Financial Reporting: Revenue tracking and system configuration

💊 Pharmacy Module
- Product Catalog: Medicine inventory with search and filtering
- Shopping Cart: Add to cart and prescription verification
- Order Management: Complete checkout and order processing
- Analytics: Sales reporting and supplier management

🔧 Platform Features
- Real‑time chat via Django Channels and ASGI
- AI symptom checker and doctor recommendations
- Secure payments via SSLCommerz sandbox
- REST APIs secured by JWT (access/refresh)
- Auto‑generated OpenAPI schema and docs
- PDF generation for reports/prescriptions (xhtml2pdf)

### 📂 Project Structure
![Project Structure](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Project%20Strcuture.jpg)





## Advantages
- End‑to‑end digital healthcare workflow in one platform
- Modular apps simplify maintenance and scaling
- Real‑time communication improves patient care
- Strong API layer for integrations and mobile clients
- Production‑friendly architecture with optional PostgreSQL/Redis

🛠️ Tech Stack
Backend
- Framework: Django 4.2.16
- API: Django REST Framework 3.14+
- Authentication: JWT (Simple JWT)
- Database: SQLite (Development), PostgreSQL (Production)
- Async: Django Channels 4.0+
- Cache: Redis (Optional)
- Task Queue: Celery (Optional)
  
  Frontend
- Templating: Django Templates
- Styling: Custom CSS with responsive design
- JavaScript: Vanilla JS for dynamic features
- Real-time: WebSockets via Django Channels
  
### Additional Packages
- API Docs: drf-spectacular (OpenAPI 3.0)
- PDF Generation: xhtml2pdf
- Payments: SSLCommerz SDK
- Environment: python-dotenv

🚀 Installation
Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtualenv (recommended)
  
Windows Installation (PowerShell)
### Clone the repository
git clone <repository-url>
cd HealthStack-System

### Create virtual environment
python -m venv venv

### Activate virtual environment
.\venv\Scripts\activate

### Install dependencies
pip install -r requirements.txt

### Environment setup
Copy-Item .env.example .env
Edit .env with your configuration
 
### Database setup
python manage.py migrate

### Create superuser
python manage.py createsuperuser

### Collect static files
python manage.py collectstatic --noinput

### Run development server
python manage.py runserver 127.0.0.1:8000

### macOS/Linux (bash)
### Clone the repository
git clone <repository-url>
cd HealthStack-System

### Create virtual environment
python3 -m venv venv

### Activate virtual environment
source venv/bin/activate

### Install dependencies
pip install -r requirements.txt

### Environment setup
cp .env.example .env
Edit .env with your configuration

### Database setup
python manage.py migrate

### Create superuser
python manage.py createsuperuser

### Collect static files
python manage.py collectstatic --noinput

### Run development server
python manage.py runserver 127.0.0.1:8000

⚙️ Configuration

Environment Variables (.env)
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

### Database (Optional - SQLite used by default)
DATABASE_URL=postgresql://username:password@localhost:5432/healthstack

### Cache (Optional)
REDIS_URL=redis://localhost:6379/0

### SSLCommerz Payments
SSLCOMMERZ_STORE_ID=your-store-id
SSLCOMMERZ_STORE_PASSWORD=your-store-password
SSLCOMMERZ_IS_SANDBOX=True

### Email (Optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

## Required Django Settings
### settings.py key configurations
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'channels',
    
    # Local apps
    'hospital',
    'doctor',
    'pharmacy',
    'ChatApp',
    'ai',
    'api',
    'sslcommerz',
]

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

### Channels configuration for WebSockets
ASGI_APPLICATION = 'HealthStack.asgi.application'
   
📱 Usage
Access Points
- Web Application: http://127.0.0.1:8000/
- Admin Interface: http://127.0.0.1:8000/admin/
- API Documentation: http://127.0.0.1:8000/api-docs/
  

### Channels configuration for WebSockets
ASGI_APPLICATION = 'HealthStack.asgi.application'

### Usage (Localhost Only)
- Start server: `python manage.py runserver 127.0.0.1:8000`
- Access web: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- Recommended `ALLOWED_HOSTS`: `['127.0.0.1', 'localhost']`
- External/mobile access and tunnels (e.g., ngrok) are disabled in this mode.

### Key Application Routes
- Patient Routes
- /login/ - Patient login
- /register/ - Patient registration
- /patient-dashboard/ - Patient dashboard
- /hospital/ - Hospital search and booking

Doctor Routes
- /doctor-login/ - Doctor authentication
- /doctor-dashboard/ - Doctor portal
- /schedule-timings/ - Availability management
- /my-patients/ - Patient management

Hospital Routes
- /hospital/ - Hospital homepage
- /hospital-dashboard/ - Admin dashboard
- /hospital-doctors/ - Doctor management
- /hospital-appointments/ - Appointment tracking

Pharmacy Routes
- /pharmacy/shop/ - Medicine catalog
- /pharmacy/cart/ - Shopping cart
- /pharmacy/checkout/ - Order processing
- /pharmacy/orders/ - Order history

  Additional Features
- /chat-home/ - Real-time messaging
- /ai/symptom-checker/ - AI health assistant
- /sslcommerz/ - Payment processing

🔌 API Documentation
Authentication
- POST /api/token/
-Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
Response:
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}

Key API Endpoints
- GET /api/ - API root with available endpoints
- GET /api/hospitals/ - List all hospitals
- GET /api/hospital/<slug>/ - Hospital details
- GET /api/doctors/ - Doctor listings
- GET /api/appointments/ - Appointment management
- GET /api/medicines/ - Pharmacy products

  API Documentation Access
  - Swagger UI: /api-docs/
  - ReDoc: /api-redoc/
  - OpenAPI Schema: /api/schema/
 
    
- Obtain JWT: `POST /api/token/` (username, password)
- Refresh token: `POST /api/token/refresh/`
- List routes: `GET /api/`
- Hospitals: `GET /api/hospitals/`
- Hospital profile: `GET /api/hospital/<slug>/`
- Docs: `/api-docs/` and `/api-redoc/` (drf‑spectacular)

### Common Commands
- Run tests: `python manage.py test`
- Collect static: `python manage.py collectstatic --noinput`


📸 Screenshots

Below are some key interface views of the **HealthStack – Hospital Management System**:
---
<<!-- screenshots:auto:start -->

🧑‍⚕️ About & Home Pages
![About](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/About.png)
![Home Page](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Home%20Page.png)

---

🔐 Authentication Pages
![Admin Login Page](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Admin%20Login%20Page.png)
![Doctor Login Page](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Doctor%20Login%20Page.png)
![Patient Login Page](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Patient%20Login%20Page.png)

---

🧭 Dashboards
![Admin Dashboard](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Admin%20Dashboard.png)
![Doctor Dashboard](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Doctor%20Dashboard.png)
![Patient Dashboard](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Patient%20Dashboard.png)

---

🏥 Hospital & Clinical Management
![Available Hospitals](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Available%20Hospitals.png)
![Available Doctors](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Available%20Doctors.png)
![Clinic And Specialist](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Clinic%20And%20Specialist.png)
![Add Clinical Technician](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Add%20Clinical%20Technician.png)

---

💊 Pharmacy & Billing
![Medicines](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Medicines.png)
![Medicine Cart](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Medicine%20Cart.png)
![Medicine Payment](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Medicine%20Payment.png)

---

 📄 Django Admin Views
![Django Administration](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Administration.png)
![Django Appointments](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Appointments.png)
![Django Add Appointment](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Add%20Appointment.png)
![Django Add Prescription](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Add%20Prescription.png)
![Django Add Report](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Add%20Report.png)
![Django Add Cart](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Add%20Cart.png)
![Django Doctor](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Doctor.png)
![Django Hospital](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Hospital.png)

---

⚙️ API and Miscellaneous
![HealthStack Api](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/HealthStack%20Api.png)
![HealthStack_Api](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/HealthStack_Api.png)
![Site Administration](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Site%20Administration.png)
![Emergency Hospitals](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Emergency%20Hospitals.png)

<!-- screenshots:auto:end -->


🚀 Deployment
- Production Considerations
- Database: Switch to PostgreSQL for production
- Static Files: Configure AWS S3 or similar service
- Media Files: Set up cloud storage
- SSL: Enable HTTPS with proper certificates
- Web Server: Use Nginx + Gunicorn/Uvicorn
- Cache: Implement Redis for better performance
- Monitoring: Set up logging and error tracking

Sample Production Settings
  ### Production configurations
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'healthstack_prod',
        'USER': 'healthstack_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

### Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

🐛 Troubleshooting
Common Issues
Static files not loading:
python manage.py collectstatic --noinput

Database migration errors:
python manage.py makemigrations
python manage.py migrate

Port already in use:
python manage.py runserver 127.0.0.1:8001

- If assets (CSS/images/fonts) do not load, verify `STATIC_URL` and paths under `static/` and run `collectstatic`.
- If you previously used ngrok and see font errors from `assets.ngrok.com`, add `?ngrok-skip-browser-warning=true` to the URL or send header `ngrok-skip-browser-warning: true` to bypass the interstitial. In localhost‑only mode, avoid ngrok entirely.
- If login fails, ensure `createsuperuser` was completed and DB migrations ran.
  
## Module import errors:
- Verify virtual environment is activated
- Check all requirements are installed: pip install -r requirements.txt
  
## Testing
  ### Run all tests
python manage.py test

### Run specific app tests
python manage.py test hospital
python manage.py test doctor
python manage.py test api


### Future Plans
- Enhanced AI diagnostics and doctor matching
- More detailed hospital analytics dashboards
- Telemedicine video consultations
- Role‑based access improvements and audit trails
- Expanded payment gateways and settlement reporting
- Docker/Kubernetes deployment examples with CI/CD

🤝 Contributing
- We welcome contributions! Please follow these steps:
- Fork the repository
- Create a feature branch: git checkout -b feature/amazing-feature
- Commit changes: git commit -m 'Add amazing feature'
- Push to branch: git push origin feature/amazing-feature
- Open a Pull Request

### Development Guidelines
- Follow PEP 8 coding standards
- Write tests for new functionality
- Update documentation for new features
- Ensure all tests pass before submitting PR

  
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🔗 Links
- Documentation: Setup Guide, Deployment Guide
- API: Live documentation available at /api-docs/
- Issue Tracking: GitHub Issues
- Releases: GitHub Releases

🏆 Acknowledgments
- Django community for excellent documentation
- Contributors and testers
- Healthcare professionals who provided domain expertise

<div align="center">
HealthStack - Transforming Healthcare Management
For support, email: shaikhmismail66@gmail.com | Documentation
</div>

                                   Made with ❤️ by K Ismail
⭐ Star this repository if you found it useful!
