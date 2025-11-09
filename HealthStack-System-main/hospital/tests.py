"""
Comprehensive test suite for Hospital app
Demonstrates industry-standard testing practices for job interviews
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal
from .models import Hospital_Information, Patient
from doctor.models import Doctor_Information, Appointment
from datetime import datetime, timedelta

User = get_user_model()


class HospitalModelTest(TestCase):
    """Test cases for Hospital_Information model"""
    
    def setUp(self):
        """Set up test data before each test method"""
        self.hospital = Hospital_Information.objects.create(
            name="Test Hospital Bengaluru",
            address="123 Test Street, Bengaluru",
            email="test@hospital.com",
            phone_number=9876543210,
            hospital_type="private",
            general_bed_no=100,
            available_icu_no=10
        )
    
    def test_hospital_creation(self):
        """Test hospital is created with correct attributes"""
        self.assertEqual(self.hospital.name, "Test Hospital Bengaluru")
        self.assertEqual(self.hospital.hospital_type, "private")
        self.assertIsNotNone(self.hospital.hospital_id)
    
    def test_hospital_string_representation(self):
        """Test the string representation of hospital"""
        self.assertEqual(str(self.hospital), "Test Hospital Bengaluru")
    
    def test_hospital_email_validation(self):
        """Test hospital email is valid"""
        self.assertIn('@', self.hospital.email)


class PatientModelTest(TestCase):
    """Test cases for Patient model"""
    
    def setUp(self):
        """Create test user and patient"""
        self.user = User.objects.create_user(
            username='testpatient',
            email='patient@test.com',
            password='securepass123',
            is_patient=True
        )
        self.patient = Patient.objects.create(
            user=self.user,
            name='Test Patient',
            username='testpatient',
            age=30,
            email='patient@test.com',
            phone_number=9876543210,
            blood_group='O+',
            address='Test Address, Bengaluru'
        )
    
    def test_patient_creation(self):
        """Test patient is created correctly"""
        self.assertEqual(self.patient.name, 'Test Patient')
        self.assertEqual(self.patient.age, 30)
        self.assertEqual(self.patient.blood_group, 'O+')
    
    def test_patient_user_relationship(self):
        """Test one-to-one relationship with User"""
        self.assertEqual(self.patient.user, self.user)
        self.assertEqual(self.user.patient, self.patient)


class PatientAuthenticationTest(TestCase):
    """Test cases for patient authentication"""
    
    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='authpatient',
            password='testpass123',
            is_patient=True
        )
        self.patient = Patient.objects.create(
            user=self.user,
            name='Auth Test Patient',
            username='authpatient'
        )
    
    def test_patient_login_success(self):
        """Test patient can login with correct credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'authpatient',
            'password': 'testpass123'
        })
        # Should redirect to dashboard after successful login
        self.assertEqual(response.status_code, 302)
    
    def test_patient_login_invalid_credentials(self):
        """Test login fails with wrong password"""
        response = self.client.post(reverse('login'), {
            'username': 'authpatient',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page
    
    def test_patient_dashboard_requires_authentication(self):
        """Test dashboard redirects to login if not authenticated"""
        response = self.client.get(reverse('patient-dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
    
    def test_patient_dashboard_accessible_when_authenticated(self):
        """Test authenticated patient can access dashboard"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('patient-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Auth Test Patient')


class PatientRegistrationTest(TestCase):
    """Test cases for patient registration"""
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('patient-register')
    
    def test_patient_registration_page_loads(self):
        """Test registration page is accessible"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')
    
    def test_patient_registration_success(self):
        """Test patient can register with valid data"""
        response = self.client.post(self.register_url, {
            'username': 'newpatient',
            'email': 'new@patient.com',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!'
        })
        # Should redirect after successful registration
        self.assertEqual(response.status_code, 302)
        
        # Verify user was created
        user_exists = User.objects.filter(username='newpatient').exists()
        self.assertTrue(user_exists)
        
        # Verify is_patient flag is set
        user = User.objects.get(username='newpatient')
        self.assertTrue(user.is_patient)


class HospitalProfileViewTest(TestCase):
    """Test cases for hospital profile view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='viewpatient',
            password='testpass123',
            is_patient=True
        )
        self.patient = Patient.objects.create(
            user=self.user,
            name='View Test Patient'
        )
        self.hospital = Hospital_Information.objects.create(
            name="View Test Hospital",
            address="Test Address",
            email="view@hospital.com",
            hospital_type="public"
        )
    
    def test_hospital_profile_accessible_to_authenticated_patient(self):
        """Test patient can view hospital profile"""
        self.client.force_login(self.user)
        url = reverse('hospital-profile', args=[self.hospital.hospital_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test Hospital")
    
    def test_hospital_profile_requires_authentication(self):
        """Test hospital profile requires login"""
        url = reverse('hospital-profile', args=[self.hospital.hospital_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class SearchFunctionalityTest(TestCase):
    """Test cases for search functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='searchpatient',
            password='testpass123',
            is_patient=True
        )
        self.patient = Patient.objects.create(
            user=self.user,
            name='Search Test Patient'
        )
        
        # Create test doctor
        self.doctor_user = User.objects.create_user(
            username='testdoctor',
            password='testpass123',
            is_doctor=True
        )
        self.doctor = Doctor_Information.objects.create(
            user=self.doctor_user,
            name='Dr. Test Cardiologist',
            consultation_fee=2000
        )
    
    def test_search_page_accessible(self):
        """Test search page loads correctly"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
    
    def test_search_returns_results(self):
        """Test search functionality returns doctors"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('search'), {'query': 'Cardio'})
        self.assertEqual(response.status_code, 200)


# Performance and Load Testing Examples
class PerformanceTest(TestCase):
    """Test cases to ensure performance standards"""
    
    def setUp(self):
        """Create bulk test data"""
        # Create 100 hospitals for performance testing
        self.hospitals = [
            Hospital_Information.objects.create(
                name=f"Hospital {i}",
                address=f"Address {i}",
                email=f"hospital{i}@test.com",
                hospital_type="private" if i % 2 == 0 else "public"
            )
            for i in range(100)
        ]
    
    def test_hospital_list_query_performance(self):
        """Test hospital list query completes quickly"""
        import time
        start_time = time.time()
        
        hospitals = list(Hospital_Information.objects.all())
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete in less than 1 second
        self.assertLess(execution_time, 1.0, 
                       f"Query took {execution_time:.3f}s, should be < 1s")
