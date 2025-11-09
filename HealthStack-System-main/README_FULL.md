# 🏥 HealthStack — Comprehensive Healthcare Management System (Full README)

## Overview

HealthStack is a modular, Django‑powered healthcare platform that unifies patients, doctors, hospitals, and pharmacies. It includes appointment scheduling, doctor and hospital profiles, an e‑pharmacy, real‑time chat, an AI symptom checker, JWT‑secured APIs with auto‑generated OpenAPI docs, and SSLCommerz payment integrations.

### Core Apps
- Hospital portal: `hospital/` — hospital homepage, profiles, search, bookings, dashboards
- Doctor portal: `doctor/` — authentication, scheduling, consultations, prescriptions, reports
- Pharmacy: `pharmacy/` — catalog, cart, orders, prescription upload, checkout
- Chat: `ChatApp/` — real‑time messaging (Django Channels/WebSockets)
- AI: `ai/` — symptom checker and doctor recommendations
- API: `api/` — DRF endpoints, JWT auth, auto docs (drf‑spectacular)
- Payments: `sslcommerz/` — payment request, success/fail/cancel flows

## Features

### Patient
- Registration, login, profile management
- Doctor search by specialization, location, rating
- Appointment booking with real‑time availability
- Digital prescriptions and medical records
- E‑pharmacy orders with prescription upload
- Real‑time chat with doctors
- Payment history and notifications

### Doctor
- Professional profile and availability management
- Appointment dashboard and schedule timings
- Create digital prescriptions and reports
- View patient history and timelines
- Earnings overview and performance insights

### Hospital Admin
- Hospital profile, departments, facilities, services
- Appointment monitoring and patient analytics
- Doctor approval and performance tracking
- Financial reports and system configuration

### Pharmacy
- Medicine catalog and inventory management
- Cart, orders, verification, and checkout flows
- Order analytics and supplier management

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