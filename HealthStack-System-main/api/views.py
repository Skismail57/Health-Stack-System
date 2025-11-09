from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import HospitalSerializer, DoctorRecommendationSerializer
from hospital.models import Hospital_Information, Patient, User 
from doctor.models import Doctor_Information
from django.urls import reverse
from ai.services import recommend_departments, recommend_doctors
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit

@api_view(['GET'])
def getRoutes(request):
    # Specify which urls (routes) to accept
    
    routes = [
        {'GET': '/api/hospital/'},
        {'GET': '/api/hospital/id'},

        # to test built-in authentication - JSON web tokens have an expiration date
        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)

# @permission_classes([IsAuthenticated]) # set up a restricted route

@api_view(['GET'])
def getHospitals(request):
    hospitals = Hospital_Information.objects.all() # query the database (get python object)
    serializer = HospitalSerializer(hospitals, many=True) # convert python object to JSON object
    # many=True because we are serializing a list of objects
    return Response(serializer.data)


@api_view(['GET'])
def getHospitalProfile(request, pk):
    hospitals = Hospital_Information.objects.get(hospital_id=pk)
    serializer = HospitalSerializer(hospitals, many=False) # many=False for a single object
    return Response(serializer.data)


@api_view(['POST'])
@ratelimit(key='ip', rate='60/m', block=True)
def recommend_doctors_api(request):
    symptoms = request.data.get('symptoms', '').strip()
    departments = recommend_departments(symptoms)
    raw_doctors = recommend_doctors(departments, limit=8)

    # Attach profile URLs
    for d in raw_doctors:
        try:
            d['profile_url'] = reverse('doctor-profile', args=[d['id']])
        except Exception:
            d['profile_url'] = ''

    serializer = DoctorRecommendationSerializer(raw_doctors, many=True)
    return Response({
        'departments': departments,
        'doctors': serializer.data,
    })


def swagger_ui(request):
    return render(request, 'api/swagger.html')
