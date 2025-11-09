"""
Quick verification command to check if everything is set up correctly
Usage: python manage.py verify_setup
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import sys


class Command(BaseCommand):
    help = 'Verify HealthStack setup and configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🔍 HEALTHSTACK SETUP VERIFICATION'))
        self.stdout.write('='*50 + '\n')
        
        issues = []
        warnings = []
        
        # Check Python version
        self.stdout.write('[1/10] Python Version...')
        if sys.version_info >= (3, 8):
            self.stdout.write(self.style.SUCCESS(f'  ✅ Python {sys.version_info.major}.{sys.version_info.minor}'))
        else:
            self.stdout.write(self.style.ERROR('  ❌ Python 3.8+ required'))
            issues.append('Python version too old')
        
        # Check Django version
        self.stdout.write('\n[2/10] Django Installation...')
        import django
        self.stdout.write(self.style.SUCCESS(f'  ✅ Django {django.VERSION[0]}.{django.VERSION[1]}'))
        
        # Check required apps
        self.stdout.write('\n[3/10] Installed Apps...')
        required_apps = [
            'rest_framework',
            'rest_framework_simplejwt.token_blacklist',
            'drf_spectacular',
            'corsheaders',
            'channels',
            'daphne',
        ]
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                self.stdout.write(self.style.SUCCESS(f'  ✅ {app}'))
            else:
                self.stdout.write(self.style.ERROR(f'  ❌ {app} not in INSTALLED_APPS'))
                issues.append(f'{app} not installed')
        
        # Check middleware
        self.stdout.write('\n[4/10] Middleware...')
        if 'corsheaders.middleware.CorsMiddleware' in settings.MIDDLEWARE:
            self.stdout.write(self.style.SUCCESS('  ✅ CORS middleware'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  CORS middleware missing'))
            warnings.append('CORS middleware not configured')
        
        # Check database
        self.stdout.write('\n[5/10] Database...')
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write(self.style.SUCCESS('  ✅ Database connected'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Database error: {str(e)}'))
            issues.append('Database connection failed')
        
        # Check Redis
        self.stdout.write('\n[6/10] Redis...')
        try:
            from django.core.cache import cache
            cache.set('test', 'test', 1)
            cache.get('test')
            self.stdout.write(self.style.SUCCESS('  ✅ Redis cache working'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Redis error: {str(e)}'))
            issues.append('Redis not running')
        
        # Check Celery
        self.stdout.write('\n[7/10] Celery...')
        if hasattr(settings, 'CELERY_BROKER_URL'):
            self.stdout.write(self.style.SUCCESS('  ✅ Celery configured'))
            self.stdout.write(f'     Broker: {settings.CELERY_BROKER_URL}')
        else:
            self.stdout.write(self.style.ERROR('  ❌ Celery not configured'))
            issues.append('Celery broker not configured')
        
        # Check Channels
        self.stdout.write('\n[8/10] Django Channels...')
        if hasattr(settings, 'CHANNEL_LAYERS'):
            self.stdout.write(self.style.SUCCESS('  ✅ Channels configured'))
        else:
            self.stdout.write(self.style.ERROR('  ❌ Channels not configured'))
            issues.append('Channels not configured')
        
        # Check CORS
        self.stdout.write('\n[9/10] CORS...')
        if hasattr(settings, 'CORS_ALLOW_ALL_ORIGINS') or hasattr(settings, 'CORS_ALLOWED_ORIGINS'):
            self.stdout.write(self.style.SUCCESS('  ✅ CORS configured'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  CORS not configured'))
            warnings.append('CORS not configured')
        
        # Check migrations
        self.stdout.write('\n[10/10] Migrations...')
        try:
            from django.db.migrations.executor import MigrationExecutor
            from django.db import connection
            executor = MigrationExecutor(connection)
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            if plan:
                self.stdout.write(self.style.WARNING(f'  ⚠️  {len(plan)} pending migrations'))
                warnings.append('Pending migrations - run: python manage.py migrate')
            else:
                self.stdout.write(self.style.SUCCESS('  ✅ All migrations applied'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Migration check failed: {str(e)}'))
        
        # Summary
        self.stdout.write('\n' + '='*50)
        
        if not issues and not warnings:
            self.stdout.write(self.style.SUCCESS('✅ ALL CHECKS PASSED!\n'))
            self.stdout.write('Your HealthStack installation is ready to use.\n')
        elif issues:
            self.stdout.write(self.style.ERROR(f'❌ {len(issues)} CRITICAL ISSUE(S) FOUND:\n'))
            for issue in issues:
                self.stdout.write(f'  • {issue}')
            self.stdout.write('')
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  {len(warnings)} WARNING(S):\n'))
            for warning in warnings:
                self.stdout.write(f'  • {warning}')
            self.stdout.write('')
        
        # Recommendations
        if issues or warnings:
            self.stdout.write('📋 RECOMMENDED ACTIONS:')
            if 'Redis not running' in [str(i) for i in issues]:
                self.stdout.write('  1. Start Redis: redis-server')
            if 'Pending migrations' in [str(w) for w in warnings]:
                self.stdout.write('  2. Run migrations: python manage.py migrate')
            if any('not installed' in str(i) for i in issues):
                self.stdout.write('  3. Install dependencies: pip install -r requirements.txt')
            self.stdout.write('')
        
        self.stdout.write('🚀 QUICK START:')
        self.stdout.write('  python manage.py migrate')
        self.stdout.write('  python manage.py setup_demo_data')
        self.stdout.write('  python manage.py test_all_features')
        self.stdout.write('  python manage.py runserver')
        self.stdout.write('')
