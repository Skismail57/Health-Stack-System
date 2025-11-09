# 🏗️ HealthStack System - Architecture Documentation

## Table of Contents
- [System Overview](#system-overview)
- [Technology Stack](#technology-stack)
- [Architecture Patterns](#architecture-patterns)
- [Database Schema](#database-schema)
- [API Architecture](#api-architecture)
- [Security Architecture](#security-architecture)
- [Scalability](#scalability)

---

## System Overview

HealthStack is a comprehensive healthcare management platform designed using modern software engineering principles and best practices.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Load Balancer                         │
│                     (Nginx/CloudFlare)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Django  │  │  Django  │  │  Django  │  │  Django  │   │
│  │  Web 1   │  │  Web 2   │  │  Web 3   │  │  Web N   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│   PostgreSQL   │  │     Redis      │  │    Celery      │
│   (Database)   │  │    (Cache)     │  │   Workers      │
└────────────────┘  └────────────────┘  └────────────────┘
```

---

## Technology Stack

### Backend
- **Framework**: Django 4.2.16
- **Language**: Python 3.11+
- **API**: Django REST Framework 3.15.2
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Real-time**: Django Channels (WebSockets)

### Database
- **Primary**: PostgreSQL 15+
- **Cache**: Redis 7+
- **ORM**: Django ORM

### Frontend
- **Template Engine**: Django Templates
- **CSS Framework**: Bootstrap 5
- **JavaScript**: Vanilla JS, AJAX

### DevOps & Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry, Prometheus
- **Web Server**: Gunicorn + Nginx
- **Task Queue**: Celery + Redis

### Third-Party Services
- **Payment Gateway**: SSLCommerz
- **Email**: SMTP (Production), Console (Development)
- **File Storage**: Local / S3-compatible

---

## Architecture Patterns

### 1. Model-View-Template (MVT)
Django's MVT pattern for web application structure:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Model     │────▶│     View     │────▶│   Template   │
│  (Data Layer)│     │  (Business)  │     │     (UI)     │
└──────────────┘     └──────────────┘     └──────────────┘
```

### 2. Multi-App Architecture
Modular design with separate Django apps:

```
healthstack/
├── hospital/         # Patient management, appointments
├── doctor/          # Doctor profiles, prescriptions
├── hospital_admin/  # Admin operations, staff management
├── pharmacy/        # Medicine inventory, orders
├── ChatApp/         # Real-time doctor-patient chat
├── api/            # RESTful API endpoints
├── ai/             # AI-powered recommendations
└── sslcommerz/     # Payment integration
```

### 3. Service-Oriented Design
Each app provides specific services:

- **hospital**: Patient registration, appointment booking, medical records
- **doctor**: Consultation, prescription creation, patient search
- **pharmacy**: Medicine management, cart system, orders
- **hospital_admin**: Staff CRUD, department management
- **ChatApp**: WebSocket-based real-time communication

### 4. Repository Pattern (Implicit)
Django ORM acts as repository layer:

```python
# Models act as repositories
patients = Patient.objects.filter(blood_group='O+')
doctors = Doctor_Information.objects.select_related('user')
```

### 5. Facade Pattern
Views serve as facades to complex business logic:

```python
def patient_dashboard(request):
    # Facade combining multiple models
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient)
    prescriptions = Prescription.objects.filter(patient=patient)
    # ... aggregate and return
```

---

## Database Schema

### Core Models

#### User Authentication
```sql
User (Django built-in)
├── username
├── email
├── password (hashed)
├── is_patient
├── is_doctor
├── is_hospital_admin
└── is_pharmacist
```

#### Hospital Domain
```sql
Hospital_Information
├── hospital_id (PK)
├── name
├── address
├── featured_image
├── email
├── phone_number
├── hospital_type
├── general_bed_no
├── available_icu_no
└── regular_cabin_no

hospital_department
├── id (PK)
├── hospital_id (FK → Hospital_Information)
├── department_name
└── created_at
```

#### Patient Domain
```sql
Patient
├── patient_id (PK)
├── user (FK → User, OneToOne)
├── name
├── age
├── email
├── phone_number
├── featured_image
├── blood_group
├── address
└── medical_history
```

#### Doctor Domain
```sql
Doctor_Information
├── doctor_id (PK)
├── user (FK → User, OneToOne)
├── name
├── specialization (FK → specialization)
├── hospital (FK → Hospital_Information)
├── consultation_fee
├── featured_image
├── degrees
└── experience_years

Appointment
├── appointment_id (PK)
├── patient (FK → Patient)
├── doctor (FK → Doctor_Information)
├── hospital (FK → Hospital_Information)
├── appointment_date
├── appointment_time
├── appointment_status
├── symptoms
└── payment_status
```

#### Prescription & Medical Records
```sql
Prescription
├── prescription_id (PK)
├── patient (FK → Patient)
├── doctor (FK → Doctor_Information)
├── appointment (FK → Appointment)
├── diagnosis
├── created_at
└── notes

Prescription_medicine
├── id (PK)
├── prescription (FK → Prescription)
├── medicine (FK → Medicine)
├── dosage
└── duration

Prescription_test
├── test_id (PK)
├── prescription (FK → Prescription)
├── test_name
├── test_fee
└── description

Lab_Report
├── report_id (PK)
├── patient (FK → Patient)
├── test (FK → Prescription_test)
├── technician (FK → Clinical_Laboratory_Technician)
├── report_file
├── findings
└── created_at
```

#### Pharmacy Domain
```sql
Medicine
├── medicine_id (PK)
├── pharmacist (FK → Pharmacist)
├── medicine_name
├── price
├── stock_quantity
├── description
└── featured_image

mediCart
├── id (PK)
├── user (FK → User)
├── medicine (FK → Medicine)
├── quantity
└── purchased (boolean)
```

### Relationships

```
User ──1:1── Patient
User ──1:1── Doctor_Information
User ──1:1── Pharmacist
User ──1:1── Clinical_Laboratory_Technician

Hospital_Information ──1:N── hospital_department
Hospital_Information ──1:N── Doctor_Information
Hospital_Information ──1:N── Appointment

Patient ──1:N── Appointment
Patient ──1:N── Prescription
Patient ──1:N── Lab_Report

Doctor_Information ──1:N── Appointment
Doctor_Information ──1:N── Prescription

Prescription ──1:N── Prescription_medicine
Prescription ──1:N── Prescription_test
```

---

## API Architecture

### RESTful Endpoints

```
Authentication:
POST   /api/users/token/          # Obtain JWT token
POST   /api/users/token/refresh/  # Refresh JWT token

Hospitals:
GET    /api/hospital/             # List all hospitals
GET    /api/hospital/<id>/        # Get hospital details

AI Recommendations:
POST   /api/recommend-doctors/    # Get doctor recommendations

Health Checks:
GET    /health/                   # Basic health check
GET    /health/ready/             # Readiness check (DB, cache)
GET    /health/live/              # Liveness check
```

### API Design Principles

1. **RESTful**: Follow REST conventions
2. **Versioned**: Support API versioning (`/api/v1/`, `/api/v2/`)
3. **Paginated**: Large lists use pagination
4. **Filtered**: Support query parameters for filtering
5. **Documented**: OpenAPI/Swagger documentation
6. **Secure**: JWT authentication, rate limiting

### Response Format

```json
{
  "status": "success",
  "data": {
    "hospital_id": 1,
    "name": "NIMHANS Hospital Bangalore",
    "address": "Bengaluru, India"
  },
  "meta": {
    "timestamp": "2024-11-07T10:30:00Z"
  }
}
```

---

## Security Architecture

### Authentication & Authorization

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ 1. Login (username, password)
       ▼
┌─────────────┐
│   Django    │
│   Backend   │
└──────┬──────┘
       │ 2. Validate & Generate JWT
       ▼
┌─────────────┐
│   Client    │ 3. Store JWT
└──────┬──────┘
       │ 4. API Request (Bearer Token)
       ▼
┌─────────────┐
│   Django    │ 5. Verify JWT & Process
│   Backend   │
└─────────────┘
```

### Security Layers

1. **Network Security**
   - HTTPS/TLS encryption
   - HSTS headers
   - Firewall rules

2. **Application Security**
   - CSRF protection
   - XSS prevention
   - SQL injection protection (ORM)
   - Rate limiting
   - Input validation

3. **Authentication**
   - Password hashing (PBKDF2)
   - JWT tokens with expiration
   - Session management

4. **Authorization**
   - Role-based access control (RBAC)
   - Permission checks
   - Object-level permissions

5. **Data Security**
   - Encrypted connections (SSL)
   - Secure password storage
   - Environment variable secrets
   - No sensitive data in logs

### Security Headers

```python
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

---

## Scalability

### Horizontal Scaling

```
                Load Balancer
                     │
        ┌────────────┼────────────┐
        │            │            │
    Django App   Django App   Django App
    Instance 1   Instance 2   Instance N
        │            │            │
        └────────────┼────────────┘
                     │
              Shared Database
                (PostgreSQL)
```

**Benefits:**
- Handle more concurrent users
- Zero-downtime deployments
- High availability
- Auto-scaling based on load

### Caching Strategy

```
Client Request
     │
     ▼
  ┌─────┐
  │Cache│ ◄── Redis (Session, Query Results)
  └─────┘
     │ Cache Miss
     ▼
  Database
```

**Cached Data:**
- Session data
- Frequently accessed queries
- Static content
- API responses

### Database Optimization

1. **Indexing**: Strategic indexes on foreign keys
2. **Query Optimization**: Use `select_related()` and `prefetch_related()`
3. **Connection Pooling**: Reuse database connections
4. **Read Replicas**: Separate read/write databases

### Asynchronous Processing

```
Web Request ──▶ Quick Response
     │
     ▼
Celery Task Queue (Background)
     │
     ├──▶ Send Email
     ├──▶ Generate Report
     ├──▶ Process Payment
     └──▶ Update Statistics
```

### Performance Targets

- **Page Load**: < 2 seconds
- **API Response**: < 200ms
- **Database Query**: < 100ms
- **Concurrent Users**: 10,000+
- **Uptime**: 99.9%

---

## Design Decisions

### Why Django?
- Rapid development
- Batteries included (admin, ORM, auth)
- Strong security features
- Large ecosystem
- Excellent documentation

### Why PostgreSQL?
- ACID compliance
- Complex queries support
- JSON field support
- Mature and stable
- Excellent Django integration

### Why Redis?
- In-memory speed
- Session storage
- Cache backend
- Celery broker
- Pub/Sub for real-time features

### Why Microservices Approach?
- Modularity
- Independent scaling
- Team autonomy
- Technology flexibility
- Easier testing

---

## Future Enhancements

1. **GraphQL API**: Alternative to REST
2. **Microservices**: Split into independent services
3. **Message Queue**: RabbitMQ for event-driven architecture
4. **Elasticsearch**: Advanced search capabilities
5. **CDN**: CloudFront for static assets
6. **Mobile Apps**: React Native / Flutter
7. **Machine Learning**: Advanced diagnosis recommendations
8. **Blockchain**: Secure medical records
9. **Telemedicine**: Video consultation integration
10. **IoT Integration**: Wearable device data

---

**Document Version**: 2.0.0  
**Last Updated**: November 2024  
**Maintained By**: HealthStack Engineering Team
