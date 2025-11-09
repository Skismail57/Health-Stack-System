from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# drf-spectacular imports
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Authentication
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API endpoints
    path('', views.getRoutes),
    path('hospital/', views.getHospitals),
    path('hospital/<int:pk>/', views.getHospitalProfile),
    path('ai/recommend-doctors/', views.recommend_doctors_api, name='api-ai-recommend-doctors'),
    
    # API Documentation (drf-spectacular)
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api-schema'), name='api-redoc'),
]
