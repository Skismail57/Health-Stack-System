from django.urls import path
from . import views


urlpatterns = [
    path('symptom-checker/', views.symptom_checker, name='symptom-checker'),
]