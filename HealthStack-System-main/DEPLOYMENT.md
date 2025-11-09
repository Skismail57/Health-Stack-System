# 🚀 Deployment Guide - HealthStack System

## Table of Contents
- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Environment Variables](#environment-variables)
- [Security Checklist](#security-checklist)

---

## Prerequisites

### Required Software
- **Python**: 3.11+
- **PostgreSQL**: 15+
- **Redis**: 7+
- **Docker** (optional): 20.10+
- **Kubernetes** (optional): 1.25+

### Required Environment Variables
```bash
SECRET_KEY=<your-secret-key>
DATABASE_URL=postgresql://user:pass@localhost:5432/healthstack
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
DEBUG=False
```

---

## Local Development

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/skismail57/healthstack.git
cd healthstack

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install  # or: pip install -r requirements.txt -r requirements-dev.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb healthstack

# Run migrations
make migrate

# Create superuser
make superuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### 3. Run Development Server

```bash
# Collect static files
make collectstatic

# Run server
make run
# Or: python manage.py runserver

# Access at: http://localhost:8000
```

---

## Docker Deployment

### Quick Start with Docker Compose

```bash
# Build and start all services
make docker-up
# Or: docker-compose up -d

# Run migrations
make docker-migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
make docker-logs

# Access at: http://localhost:8000
```

### Production Docker Build

```bash
# Build production image
docker build -t healthstack:v1.0 .

# Run with production settings
docker run -d \
  -p 8000:8000 \
  -e DJANGO_SETTINGS_MODULE=healthstack.settings_production \
  -e DATABASE_URL=postgresql://user:pass@db:5432/healthstack \
  -e REDIS_URL=redis://redis:6379/0 \
  healthstack:v1.0
```

---

## Kubernetes Deployment

### 1. Create Secrets

```bash
# Create secret for sensitive data
kubectl create secret generic healthstack-secrets \
  --from-literal=secret-key='your-secret-key' \
  --from-literal=database-url='postgresql://user:pass@db:5432/healthstack' \
  --from-literal=db-user='healthstack' \
  --from-literal=db-password='your-password'
```

### 2. Deploy Database and Redis

```bash
# Deploy PostgreSQL
kubectl apply -f k8s/postgres.yaml

# Deploy Redis
kubectl apply -f k8s/redis.yaml

# Wait for services to be ready
kubectl wait --for=condition=ready pod -l component=database --timeout=300s
kubectl wait --for=condition=ready pod -l component=cache --timeout=300s
```

### 3. Deploy Application

```bash
# Deploy web application
kubectl apply -f k8s/deployment.yaml

# Deploy ingress
kubectl apply -f k8s/ingress.yaml

# Check deployment status
kubectl get pods
kubectl get services
kubectl get ingress
```

### 4. Run Migrations

```bash
# Get pod name
POD_NAME=$(kubectl get pods -l app=healthstack,component=web -o jsonpath='{.items[0].metadata.name}')

# Run migrations
kubectl exec -it $POD_NAME -- python manage.py migrate

# Create superuser
kubectl exec -it $POD_NAME -- python manage.py createsuperuser

# Collect static files
kubectl exec -it $POD_NAME -- python manage.py collectstatic --noinput
```

### 5. Scale Application

```bash
# Manual scaling
kubectl scale deployment healthstack-web --replicas=5

# Auto-scaling is configured via HPA in deployment.yaml
# Check HPA status
kubectl get hpa
```

---

## Cloud Deployment

### AWS (Amazon Web Services)

#### Using AWS ECS + RDS + ElastiCache

```bash
# 1. Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier healthstack-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username healthstack \
  --master-user-password YourPassword123

# 2. Create ElastiCache Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id healthstack-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1

# 3. Push Docker image to ECR
aws ecr create-repository --repository-name healthstack
docker tag healthstack:latest <account-id>.dkr.ecr.region.amazonaws.com/healthstack:latest
docker push <account-id>.dkr.ecr.region.amazonaws.com/healthstack:latest

# 4. Create ECS task definition and service
aws ecs create-cluster --cluster-name healthstack-cluster
# Use AWS Console or CloudFormation for detailed setup
```

### Google Cloud Platform (GCP)

```bash
# 1. Create Cloud SQL PostgreSQL instance
gcloud sql instances create healthstack-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

# 2. Create GKE cluster
gcloud container clusters create healthstack-cluster \
  --num-nodes=3 \
  --zone=us-central1-a

# 3. Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/healthstack

# 4. Deploy to GKE
kubectl apply -f k8s/
```

### Microsoft Azure

```bash
# 1. Create Azure Database for PostgreSQL
az postgres server create \
  --resource-group healthstack-rg \
  --name healthstack-db \
  --location eastus \
  --admin-user healthstack \
  --admin-password YourPassword123 \
  --sku-name B_Gen5_1

# 2. Create Azure Cache for Redis
az redis create \
  --resource-group healthstack-rg \
  --name healthstack-redis \
  --location eastus \
  --sku Basic \
  --vm-size c0

# 3. Deploy to Azure Container Instances or AKS
az container create \
  --resource-group healthstack-rg \
  --name healthstack-web \
  --image healthstack:latest \
  --dns-name-label healthstack \
  --ports 8000
```

### DigitalOcean

```bash
# 1. Create Managed PostgreSQL Database
doctl databases create healthstack-db --engine pg --region nyc1

# 2. Create Managed Redis Cluster
doctl databases create healthstack-redis --engine redis --region nyc1

# 3. Push to DigitalOcean Container Registry
doctl registry create healthstack-registry
docker tag healthstack:latest registry.digitalocean.com/healthstack/web:latest
docker push registry.digitalocean.com/healthstack/web:latest

# 4. Deploy to App Platform
doctl apps create --spec .do/app.yaml
```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `REDIS_URL` | Redis connection string | `redis://host:6379/0` |
| `ALLOWED_HOSTS` | Comma-separated hostnames | `localhost,example.com` |
| `DEBUG` | Debug mode (False in production) | `False` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EMAIL_HOST` | SMTP server | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_HOST_USER` | Email username | - |
| `EMAIL_HOST_PASSWORD` | Email password | - |
| `SENTRY_DSN` | Sentry error tracking DSN | - |
| `AWS_ACCESS_KEY_ID` | AWS S3 access key | - |
| `AWS_SECRET_ACCESS_KEY` | AWS S3 secret key | - |

---

## Security Checklist

### Before Production Deployment

- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY` (50+ characters)
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Enable HTTPS/SSL (`SECURE_SSL_REDIRECT=True`)
- [ ] Set secure cookies (`SESSION_COOKIE_SECURE=True`)
- [ ] Enable HSTS (`SECURE_HSTS_SECONDS=31536000`)
- [ ] Configure CORS if using separate frontend
- [ ] Use environment variables for secrets (never commit to git)
- [ ] Setup database backups
- [ ] Configure monitoring (Sentry, CloudWatch, etc.)
- [ ] Enable rate limiting
- [ ] Review file upload security
- [ ] Check SQL injection protection (use ORM)
- [ ] Validate all user inputs
- [ ] Setup firewall rules
- [ ] Use strong database passwords
- [ ] Enable database SSL connections
- [ ] Setup regular security scans
- [ ] Configure CSP headers
- [ ] Enable audit logging
- [ ] Review API authentication

### SSL/TLS Certificate Setup

```bash
# Using Let's Encrypt with Certbot
certbot --nginx -d healthstack.example.com

# Or in Kubernetes with cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

---

## Monitoring and Maintenance

### Health Checks

```bash
# Check application health
curl http://localhost:8000/health/

# Check readiness (includes DB, cache)
curl http://localhost:8000/health/ready/

# Check liveness
curl http://localhost:8000/health/live/
```

### Database Backup

```bash
# Backup
make db-backup

# Restore
make db-restore

# PostgreSQL direct backup
pg_dump healthstack > backup_$(date +%Y%m%d).sql

# PostgreSQL restore
psql healthstack < backup_20240101.sql
```

### Log Management

```bash
# View application logs
tail -f logs/django.log

# Docker logs
docker-compose logs -f web

# Kubernetes logs
kubectl logs -f deployment/healthstack-web
```

---

## Performance Optimization

### Database Optimization

```bash
# Create indexes
python manage.py dbshell
CREATE INDEX idx_patient_user ON hospital_patient(user_id);
CREATE INDEX idx_doctor_hospital ON doctor_information(hospital_id);

# Analyze query performance
python manage.py shell
from django.db import connection
print(connection.queries)
```

### Caching Setup

```python
# settings.py - Already configured in settings_production.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
    }
}
```

### Static Files CDN

```python
# Configure AWS S3 for static files
AWS_STORAGE_BUCKET_NAME = 'healthstack-static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

---

## Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check DATABASE_URL
echo $DATABASE_URL

# Test PostgreSQL connection
psql $DATABASE_URL

# Check PostgreSQL is running
systemctl status postgresql
```

**Redis Connection Error**
```bash
# Test Redis connection
redis-cli ping

# Check Redis is running
systemctl status redis
```

**Static Files Not Loading**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT setting
python manage.py diffsettings | grep STATIC
```

---

## Support

- **Documentation**: https://github.com/yourusername/healthstack/wiki
- **Issues**: https://github.com/yourusername/healthstack/issues
- **Email**: support@healthstack.com

---

**Last Updated**: 2024
**Version**: 2.0.0
