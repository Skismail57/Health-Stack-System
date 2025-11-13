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

### Platform
- Real‑time chat via Django Channels and ASGI
- AI symptom checker and doctor recommendations
- Secure payments via SSLCommerz sandbox
- REST APIs secured by JWT (access/refresh)
- Auto‑generated OpenAPI schema and docs
- PDF generation for reports/prescriptions (xhtml2pdf)

## Advantages
- End‑to‑end digital healthcare workflow in one platform
- Modular apps simplify maintenance and scaling
- Real‑time communication improves patient care
- Strong API layer for integrations and mobile clients
- Production‑friendly architecture with optional PostgreSQL/Redis

## Tech Used
- Django `4.2.16`
- Django REST Framework
- drf‑spectacular (OpenAPI)
- Django Channels + ASGI (WebSockets)
- Daphne (ASGI server; production optional)
- Celery (background tasks; optional)
- xhtml2pdf (PDF)
- HTML/CSS/JS templates
- SQLite (dev), PostgreSQL and Redis optional in production

## Installation

### Windows (PowerShell)
```
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

### macOS/Linux (bash)
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

### Environment
```
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
# Optional:
DATABASE_URL=postgresql://user:pass@localhost:5432/healthstack
REDIS_URL=redis://localhost:6379/0
SSLCOMMERZ_STORE_ID=your-store-id
SSLCOMMERZ_STORE_PASSWORD=your-password
SSLCOMMERZ_IS_SANDBOX=True
```

## Usage (Localhost Only)
- Start server: `python manage.py runserver 127.0.0.1:8000`
- Access web: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- Recommended `ALLOWED_HOSTS`: `['127.0.0.1', 'localhost']`
- External/mobile access and tunnels (e.g., ngrok) are disabled in this mode.

### Key Routes
- Home: `/`
- Login: `/login/`
- Hospital: `/hospital/` and related pages
- Doctor: `/doctor/`, `doctor-login/`, `doctor-dashboard/`, `schedule-timings/`
- Pharmacy: `/pharmacy/shop/`, `/pharmacy/cart/`, `/pharmacy/checkout/`
- Chat: `/chat-home/`
- AI: `/ai/symptom-checker/`
- Payment: `/sslcommerz/`

### API
- Obtain JWT: `POST /api/token/` (username, password)
- Refresh token: `POST /api/token/refresh/`
- List routes: `GET /api/`
- Hospitals: `GET /api/hospitals/`
- Hospital profile: `GET /api/hospital/<slug>/`
- Docs: `/api-docs/` and `/api-redoc/` (drf‑spectacular)

### Common Commands
- Run tests: `python manage.py test`
- Collect static: `python manage.py collectstatic --noinput`

## Screenshots

<<!-- screenshots:auto:start -->

## 📸 Screenshots

Below are some key interface views of the **HealthStack – Hospital Management System**:

---

### 🧑‍⚕️ About & Home Pages
![About](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/About.png)
![Home Page](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Home%20Page.png)

---

### 🔐 Authentication Pages
![Admin Login Page](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Admin%20Login%20Page.png)
![Doctor Login Page](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Doctor%20Login%20Page.png)
![Patient Login Page](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Patient%20Login%20Page.png)

---

### 🧭 Dashboards
![Admin Dashboard](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Admin%20Dashboard.png)
![Doctor Dashboard](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Doctor%20Dashboard.png)
![Patient Dashboard](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Patient%20Dashboard.png)

---

### 🏥 Hospital & Clinical Management
![Available Hospitals](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Available%20Hospitals.png)
![Available Doctors](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Available%20Doctors.png)
![Clinic And Specialist](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Clinic%20And%20Specialist.png)
![Add Clinical Technician](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Add%20Clinical%20Technician.png)

---

### 💊 Pharmacy & Billing
![Medicines](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Medicines.png)
![Medicine Cart](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Medicine%20Cart.png)
![Medicine Payment](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Medicine%20Payment.png)

---

### 📄 Django Admin Views
![Django Administration](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Administration.png)
![Django Appointments](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Appointments.png)
![Django Add Appointment](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Add%20Appointment.png)
![Django Add Prescription](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Add%20Prescription.png)
![Django Add Report](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Add%20Report.png)
![Django Add Cart](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Add%20Cart.png)
![Django Doctor](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Doctor.png)
![Django Hospital](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Django%20Hospital.png)

---

### ⚙️ API and Miscellaneous
![HealthStack Api](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/HealthStack%20Api.png)
![HealthStack_Api](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/HealthStack_Api.png)
![Site Administration](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Site%20Administration.png)
![Emergency Hospitals](https://raw.githubusercontent.com/Skismail57/Health-Stack-System/main/HealthStack-System-main/static/Screenshots/Emergency%20Hospitals.png)




<!-- screenshots:auto:end -->



Place PNG/JPG files in `static/screenshots/` using these suggested names:
- `banner.png`, `homepage.png`, `patient-dashboard.png`
- `doctor-profile.png`, `appointment-booking.png`, `prescription.png`
- `pharmacy.png`, `chat.png`, `admin-dashboard.png`, `payment.png`

Embed in Markdown using:
```
![Homepage](static/screenshots/homepage.png)
```

## Troubleshooting
- If assets (CSS/images/fonts) do not load, verify `STATIC_URL` and paths under `static/` and run `collectstatic`.
- If you previously used ngrok and see font errors from `assets.ngrok.com`, add `?ngrok-skip-browser-warning=true` to the URL or send header `ngrok-skip-browser-warning: true` to bypass the interstitial. In localhost‑only mode, avoid ngrok entirely.
- If login fails, ensure `createsuperuser` was completed and DB migrations ran.

## Future Plans
- Enhanced AI diagnostics and doctor matching
- More detailed hospital analytics dashboards
- Telemedicine video consultations
- Role‑based access improvements and audit trails
- Expanded payment gateways and settlement reporting
- Docker/Kubernetes deployment examples with CI/CD

## Contributing
- Fork the repo and create feature branches
- Run tests before submitting PRs
- Keep changes focused and documented

## Links
- Setup: `SETUP_GUIDE.md`
- Deployment: `DEPLOYMENT.md`
- APIs: `/api/`, `/api-docs/`, `/api-redoc/`
