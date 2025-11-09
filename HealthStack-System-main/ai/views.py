from django.shortcuts import render
from .services import recommend_departments, recommend_doctors


def symptom_checker(request):
    result = []
    recommended_doctors = []
    symptoms = ""
    if request.method == "POST":
        symptoms = request.POST.get("symptoms", "").strip()
        result = recommend_departments(symptoms)
        recommended_doctors = recommend_doctors(result, limit=8)
    return render(request, 'ai/symptom_checker.html', {
        'result': result,
        'symptoms': symptoms,
        'recommended_doctors': recommended_doctors,
    })