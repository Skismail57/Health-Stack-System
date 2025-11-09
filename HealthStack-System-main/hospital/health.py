"""
Health Check Endpoints for Load Balancers and Monitoring
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import sys


def health_check(request):
    """
    Basic health check endpoint
    Returns: 200 OK if service is healthy
    """
    health_status = {
        'status': 'healthy',
        'service': 'healthstack',
        'version': '2.0.0'
    }
    return JsonResponse(health_status)


def readiness_check(request):
    """
    Readiness check - checks if app is ready to serve traffic
    Verifies database and cache connectivity
    """
    checks = {
        'database': check_database(),
        'cache': check_cache(),
    }
    
    all_healthy = all(checks.values())
    
    response_data = {
        'status': 'ready' if all_healthy else 'not_ready',
        'checks': checks,
        'version': '2.0.0'
    }
    
    status_code = 200 if all_healthy else 503
    return JsonResponse(response_data, status=status_code)


def liveness_check(request):
    """
    Liveness check - checks if app is alive
    Simple check that returns 200 if process is running
    """
    return JsonResponse({
        'status': 'alive',
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    })


def check_database():
    """Check database connection"""
    try:
        connection.ensure_connection()
        return True
    except Exception as e:
        print(f"Database check failed: {e}")
        return False


def check_cache():
    """Check cache connection (Redis/Memcached)"""
    try:
        cache.set('health_check', 'ok', 10)
        result = cache.get('health_check')
        return result == 'ok'
    except Exception as e:
        print(f"Cache check failed: {e}")
        return False
