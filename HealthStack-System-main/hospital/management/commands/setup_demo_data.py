"""
Management command to create demo data for testing
Usage: python manage.py setup_demo_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from hospital.models import Hospital_Information, Patient
from doctor.models import Doctor_Information
from pharmacy.models import Medicine
from datetime import datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Create demo data for HealthStack testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete existing demo data before creating new',
        )

    def handle(self, *args, **options):
        flush = options.get('flush', False)
        
        self.stdout.write(self.style.SUCCESS('\n🏥 HEALTHSTACK DEMO DATA SETUP'))
        self.stdout.write('='*50 + '\n')
        
        if flush:
            self.stdout.write(self.style.WARNING('⚠️  Flushing existing demo data...'))
            # Be careful with this in production
            User.objects.filter(username__startswith='demo_').delete()
            Hospital_Information.objects.filter(name__startswith='Demo').delete()
        
        # Create Admin User
        self.stdout.write('\n[1/5] Creating Admin User...')
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@healthstack.com',
                'is_staff': True,
                'is_superuser': True,
                'is_admin': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('  ✅ Admin created: admin / admin123'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  Admin already exists'))
        
        # Create Demo Hospital
        self.stdout.write('\n[2/5] Creating Demo Hospital...')
        hospital, created = Hospital_Information.objects.get_or_create(
            name='Demo General Hospital',
            defaults={
                'location': 'New York, NY',
                'contact': '+1-555-0100',
                'email': 'info@demohospital.com',
                'description': 'A comprehensive healthcare facility',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  ✅ Hospital created: Demo General Hospital'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  Hospital already exists'))
        
        # Create Demo Doctor
        self.stdout.write('\n[3/5] Creating Demo Doctor...')
        doctor_user, created = User.objects.get_or_create(
            username='demo_doctor',
            defaults={
                'email': 'doctor@healthstack.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'is_doctor': True,
            }
        )
        if created:
            doctor_user.set_password('doctor123')
            doctor_user.save()
            self.stdout.write(self.style.SUCCESS('  ✅ Doctor user: demo_doctor / doctor123'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  Doctor user already exists'))
        
        # Create Doctor Profile
        doctor_profile, created = Doctor_Information.objects.get_or_create(
            user=doctor_user,
            defaults={
                'hospital': hospital,
                'department': 'General Medicine',
                'specialization': 'Family Medicine',
                'qualification': 'MD, MBBS',
                'experience': 10,
                'fees': 100.00,
                'contact': '+1-555-0101',
                'email': doctor_user.email,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  ✅ Doctor profile created'))
        
        # Create Demo Patient
        self.stdout.write('\n[4/5] Creating Demo Patient...')
        patient_user, created = User.objects.get_or_create(
            username='demo_patient',
            defaults={
                'email': 'patient@healthstack.com',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'is_patient': True,
            }
        )
        if created:
            patient_user.set_password('patient123')
            patient_user.save()
            self.stdout.write(self.style.SUCCESS('  ✅ Patient user: demo_patient / patient123'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  Patient user already exists'))
        
        # Create Patient Profile
        patient_profile, created = Patient.objects.get_or_create(
            user=patient_user,
            defaults={
                'name': f'{patient_user.first_name} {patient_user.last_name}',
                'age': 30,
                'gender': 'Female',
                'contact': '+1-555-0102',
                'email': patient_user.email,
                'address': '123 Main St, New York, NY',
                'blood_group': 'A+',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  ✅ Patient profile created'))
        
        # Create Demo Medicines
        self.stdout.write('\n[5/5] Creating Demo Medicines...')
        medicines = [
            {'name': 'Paracetamol', 'category': 'Pain Relief', 'price': 5.99, 'stock': 1000},
            {'name': 'Amoxicillin', 'category': 'Antibiotic', 'price': 12.99, 'stock': 500},
            {'name': 'Ibuprofen', 'category': 'Pain Relief', 'price': 8.99, 'stock': 750},
            {'name': 'Omeprazole', 'category': 'Digestive', 'price': 15.99, 'stock': 300},
            {'name': 'Metformin', 'category': 'Diabetes', 'price': 20.99, 'stock': 400},
        ]
        
        created_count = 0
        for med_data in medicines:
            med, created = Medicine.objects.get_or_create(
                name=med_data['name'],
                defaults=med_data
            )
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ {created_count} medicines created'))
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('✅ DEMO DATA SETUP COMPLETE!\n'))
        
        self.stdout.write('📋 Login Credentials:')
        self.stdout.write('  Admin:   admin / admin123')
        self.stdout.write('  Doctor:  demo_doctor / doctor123')
        self.stdout.write('  Patient: demo_patient / patient123')
        self.stdout.write('')
        self.stdout.write('🌐 Access Points:')
        self.stdout.write('  Admin:   http://localhost:8000/admin/')
        self.stdout.write('  Login:   http://localhost:8000/login/')
        self.stdout.write('  API:     http://localhost:8000/api/')
        self.stdout.write('  Docs:    http://localhost:8000/api/docs/')
        self.stdout.write('')
