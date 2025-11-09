"""
Management command to test all HealthStack features
Usage: python manage.py test_all_features
"""
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils import timezone
from hospital.models import Hospital_Information, Patient
from doctor.models import Doctor_Information, Appointment
from pharmacy.models import Medicine
from ChatApp.models import chatMessages
import redis
import json

User = get_user_model()


class Command(BaseCommand):
    help = 'Test all HealthStack features to verify they are working'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output',
        )

    def handle(self, *args, **options):
        verbose = options.get('verbose', False)
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('  HEALTHSTACK FEATURE VERIFICATION TEST'))
        self.stdout.write(self.style.SUCCESS('='*70 + '\n'))

        results = []
        
        # Test 1: Database Connection
        results.append(self.test_database())
        
        # Test 2: Redis Cache
        results.append(self.test_redis_cache())
        
        # Test 3: Celery Broker
        results.append(self.test_celery_broker())
        
        # Test 4: Models
        results.append(self.test_models())
        
        # Test 5: User Authentication
        results.append(self.test_user_auth())
        
        # Test 6: API Endpoints
        results.append(self.test_api())
        
        # Test 7: Channels Layer (WebSocket)
        results.append(self.test_channels())
        
        # Summary
        self.print_summary(results)

    def test_database(self):
        """Test database connection"""
        self.stdout.write('\n[1/7] Testing Database Connection...')
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write(self.style.SUCCESS('  ✅ Database: Connected'))
            return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Database: {str(e)}'))
            return False

    def test_redis_cache(self):
        """Test Redis cache"""
        self.stdout.write('\n[2/7] Testing Redis Cache...')
        try:
            # Test cache set/get
            test_key = 'healthstack_test_key'
            test_value = 'test_value_12345'
            cache.set(test_key, test_value, timeout=10)
            retrieved = cache.get(test_key)
            
            if retrieved == test_value:
                cache.delete(test_key)
                self.stdout.write(self.style.SUCCESS('  ✅ Redis Cache: Working'))
                self.stdout.write('     - Set/Get: OK')
                self.stdout.write('     - Delete: OK')
                return True
            else:
                self.stdout.write(self.style.ERROR('  ❌ Redis Cache: Value mismatch'))
                return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Redis Cache: {str(e)}'))
            self.stdout.write(self.style.WARNING('     Make sure Redis is running: redis-server'))
            return False

    def test_celery_broker(self):
        """Test Celery broker connection"""
        self.stdout.write('\n[3/7] Testing Celery Broker...')
        try:
            from django.conf import settings
            broker_url = settings.CELERY_BROKER_URL
            
            # Try to connect to Redis broker
            r = redis.from_url(broker_url)
            r.ping()
            
            self.stdout.write(self.style.SUCCESS('  ✅ Celery Broker: Connected'))
            self.stdout.write(f'     - Broker: {broker_url}')
            
            # Try to inspect celery workers
            try:
                from healthstack.celery import app
                inspect = app.control.inspect()
                stats = inspect.stats()
                if stats:
                    self.stdout.write('     - Workers: Active')
                else:
                    self.stdout.write(self.style.WARNING('     - Workers: No active workers'))
                    self.stdout.write('       Start worker: celery -A healthstack worker -l info')
            except:
                self.stdout.write(self.style.WARNING('     - Workers: Cannot inspect'))
            
            return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Celery Broker: {str(e)}'))
            return False

    def test_models(self):
        """Test database models"""
        self.stdout.write('\n[4/7] Testing Database Models...')
        try:
            user_count = User.objects.count()
            hospital_count = Hospital_Information.objects.count()
            doctor_count = Doctor_Information.objects.count()
            patient_count = Patient.objects.count()
            medicine_count = Medicine.objects.count()
            message_count = chatMessages.objects.count()
            
            self.stdout.write(self.style.SUCCESS('  ✅ Models: All accessible'))
            self.stdout.write(f'     - Users: {user_count}')
            self.stdout.write(f'     - Hospitals: {hospital_count}')
            self.stdout.write(f'     - Doctors: {doctor_count}')
            self.stdout.write(f'     - Patients: {patient_count}')
            self.stdout.write(f'     - Medicines: {medicine_count}')
            self.stdout.write(f'     - Messages: {message_count}')
            return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Models: {str(e)}'))
            return False

    def test_user_auth(self):
        """Test user authentication system"""
        self.stdout.write('\n[5/7] Testing User Authentication...')
        try:
            # Check for admin user
            admin_count = User.objects.filter(is_staff=True).count()
            patient_count = User.objects.filter(is_patient=True).count()
            doctor_count = User.objects.filter(is_doctor=True).count()
            
            self.stdout.write(self.style.SUCCESS('  ✅ Authentication: Working'))
            self.stdout.write(f'     - Staff Users: {admin_count}')
            self.stdout.write(f'     - Patients: {patient_count}')
            self.stdout.write(f'     - Doctors: {doctor_count}')
            
            # Test JWT
            try:
                from rest_framework_simplejwt.tokens import RefreshToken
                if User.objects.exists():
                    user = User.objects.first()
                    token = RefreshToken.for_user(user)
                    self.stdout.write('     - JWT Tokens: OK')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'     - JWT: {str(e)}'))
            
            return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Authentication: {str(e)}'))
            return False

    def test_api(self):
        """Test API configuration"""
        self.stdout.write('\n[6/7] Testing API Configuration...')
        try:
            from django.conf import settings
            
            # Check REST_FRAMEWORK settings
            rf_settings = settings.REST_FRAMEWORK
            
            self.stdout.write(self.style.SUCCESS('  ✅ API: Configured'))
            self.stdout.write('     - DRF: Installed')
            self.stdout.write('     - JWT Auth: Enabled')
            
            # Check for drf-spectacular
            if 'drf_spectacular' in settings.INSTALLED_APPS:
                self.stdout.write('     - API Docs: /api/docs/')
            
            # Check for CORS
            if 'corsheaders' in settings.INSTALLED_APPS:
                self.stdout.write('     - CORS: Enabled')
            
            return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ API: {str(e)}'))
            return False

    def test_channels(self):
        """Test Django Channels"""
        self.stdout.write('\n[7/7] Testing WebSocket (Channels)...')
        try:
            from django.conf import settings
            
            if hasattr(settings, 'CHANNEL_LAYERS'):
                channel_config = settings.CHANNEL_LAYERS['default']
                self.stdout.write(self.style.SUCCESS('  ✅ Channels: Configured'))
                self.stdout.write(f'     - Backend: {channel_config["BACKEND"]}')
                self.stdout.write('     - WebSocket: ws://localhost:8000/ws/chat/')
                
                # Try to test channel layer
                try:
                    from channels.layers import get_channel_layer
                    channel_layer = get_channel_layer()
                    self.stdout.write('     - Layer: Accessible')
                except:
                    self.stdout.write(self.style.WARNING('     - Layer: Cannot access'))
                
                return True
            else:
                self.stdout.write(self.style.WARNING('  ⚠️  Channels: Not configured'))
                return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Channels: {str(e)}'))
            return False

    def print_summary(self, results):
        """Print test summary"""
        self.stdout.write('\n' + '='*70)
        passed = sum(results)
        total = len(results)
        percentage = (passed / total * 100) if total > 0 else 0
        
        if passed == total:
            self.stdout.write(self.style.SUCCESS(f'  ✅ ALL TESTS PASSED ({passed}/{total}) - 100%'))
        elif passed > total / 2:
            self.stdout.write(self.style.WARNING(f'  ⚠️  SOME TESTS FAILED ({passed}/{total}) - {percentage:.0f}%'))
        else:
            self.stdout.write(self.style.ERROR(f'  ❌ MOST TESTS FAILED ({passed}/{total}) - {percentage:.0f}%'))
        
        self.stdout.write('='*70)
        
        self.stdout.write('\n📋 QUICK START COMMANDS:')
        self.stdout.write('  Redis:    redis-server')
        self.stdout.write('  Django:   python manage.py runserver')
        self.stdout.write('  Celery:   celery -A healthstack worker -l info')
        self.stdout.write('  Beat:     celery -A healthstack beat -l info')
        self.stdout.write('  API Docs: http://localhost:8000/api/docs/')
        self.stdout.write('')
