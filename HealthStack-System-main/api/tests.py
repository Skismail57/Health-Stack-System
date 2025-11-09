"""
API Test Suite - RESTful API Testing
Demonstrates modern API testing practices
"""
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from hospital.models import Hospital_Information, Patient
from doctor.models import Doctor_Information
from django.urls import reverse

User = get_user_model()


class HospitalAPITest(APITestCase):
    """Test cases for Hospital API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.hospital = Hospital_Information.objects.create(
            name="API Test Hospital",
            address="123 API Street",
            email="api@hospital.com",
            hospital_type="private"
        )
    
    def test_get_hospitals_list(self):
        """Test GET /api/hospital/ returns hospital list"""
        url = reverse('hospitals')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
    
    def test_get_hospital_detail(self):
        """Test GET /api/hospital/<id> returns hospital details"""
        url = reverse('hospital', args=[self.hospital.hospital_id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "API Test Hospital")
        self.assertEqual(response.data['hospital_type'], "private")
    
    def test_get_nonexistent_hospital(self):
        """Test GET with invalid ID returns 404"""
        url = reverse('hospital', args=[99999])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_hospital_list_performance(self):
        """Test API response time is acceptable"""
        # Create multiple hospitals
        for i in range(50):
            Hospital_Information.objects.create(
                name=f"Hospital {i}",
                email=f"hospital{i}@test.com",
                hospital_type="public"
            )
        
        import time
        url = reverse('hospitals')
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        
        execution_time = end_time - start_time
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(execution_time, 2.0, "API response should be < 2 seconds")


class AuthenticationAPITest(APITestCase):
    """Test JWT authentication"""
    
    def setUp(self):
        """Create test user"""
        self.user = User.objects.create_user(
            username='apiuser',
            password='testpass123',
            email='api@user.com'
        )
        self.client = APIClient()
    
    def test_obtain_jwt_token(self):
        """Test POST /api/users/token/ returns JWT tokens"""
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': 'apiuser',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_refresh_jwt_token(self):
        """Test POST /api/users/token/refresh/ refreshes token"""
        # First get tokens
        token_url = reverse('token_obtain_pair')
        token_response = self.client.post(token_url, {
            'username': 'apiuser',
            'password': 'testpass123'
        })
        refresh_token = token_response.data['refresh']
        
        # Then refresh
        refresh_url = reverse('token_refresh')
        response = self.client.post(refresh_url, {
            'refresh': refresh_token
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_jwt_token_invalid_credentials(self):
        """Test JWT token with wrong credentials"""
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': 'apiuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DoctorRecommendationAPITest(APITestCase):
    """Test AI-powered doctor recommendation API"""
    
    def setUp(self):
        """Create test doctors"""
        self.client = APIClient()
        
        # Create test doctor
        doctor_user = User.objects.create_user(
            username='cardio_doctor',
            password='test123',
            is_doctor=True
        )
        self.doctor = Doctor_Information.objects.create(
            user=doctor_user,
            name='Dr. Heart Specialist',
            consultation_fee=2500
        )
    
    def test_recommend_doctors_api(self):
        """Test POST /api/recommend-doctors/ returns recommendations"""
        url = reverse('recommend-doctors')
        response = self.client.post(url, {
            'symptoms': 'chest pain and irregular heartbeat'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('departments', response.data)
        self.assertIn('doctors', response.data)
    
    def test_recommend_doctors_empty_symptoms(self):
        """Test API handles empty symptoms"""
        url = reverse('recommend-doctors')
        response = self.client.post(url, {
            'symptoms': ''
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIRateLimitingTest(APITestCase):
    """Test API rate limiting (if implemented)"""
    
    def test_api_handles_multiple_requests(self):
        """Test API can handle burst of requests"""
        url = reverse('hospitals')
        
        # Make 20 rapid requests
        for i in range(20):
            response = self.client.get(url)
            # Should not fail even with many requests
            self.assertIn(response.status_code, [200, 429])  # 429 = Too Many Requests


class APISerializerTest(APITestCase):
    """Test API serializers return correct data format"""
    
    def setUp(self):
        self.hospital = Hospital_Information.objects.create(
            name="Serializer Test Hospital",
            email="serializer@test.com",
            hospital_type="private",
            general_bed_no=100
        )
    
    def test_hospital_serializer_fields(self):
        """Test hospital serializer includes all required fields"""
        url = reverse('hospital', args=[self.hospital.hospital_id])
        response = self.client.get(url)
        
        required_fields = ['hospital_id', 'name', 'email', 'hospital_type']
        for field in required_fields:
            self.assertIn(field, response.data)
    
    def test_serializer_data_types(self):
        """Test serializer returns correct data types"""
        url = reverse('hospital', args=[self.hospital.hospital_id])
        response = self.client.get(url)
        
        self.assertIsInstance(response.data['name'], str)
        self.assertIsInstance(response.data['hospital_id'], int)
        self.assertIsInstance(response.data['general_bed_no'], int)
