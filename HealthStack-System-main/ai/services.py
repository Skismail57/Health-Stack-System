from typing import List, Sequence
from django.db.models import Q
from doctor.models import Doctor_Information


# Minimal keyword-to-department rules. Extendable with ML later.
SYMPTOM_MAP = {
    'chest pain': ['Cardiology'],
    'palpitations': ['Cardiology'],
    'shortness of breath': ['Cardiology', 'General Medicine'],
    'heart': ['Cardiology'],
    'rash': ['Dermatology'],
    'itchy skin': ['Dermatology'],
    'acne': ['Dermatology'],
    'skin': ['Dermatology'],
    'tooth': ['Dentistry'],
    'gum': ['Dentistry'],
    'back pain': ['Orthopedics'],
    'joint pain': ['Orthopedics'],
    'fracture': ['Orthopedics'],
    'fever': ['General Medicine', 'Pediatrics'],
    'cough': ['General Medicine', 'Pediatrics'],
    'cold': ['General Medicine', 'Pediatrics'],
    'child': ['Pediatrics'],
    'numbness': ['Neurology'],
    'migraine': ['Neurology'],
    'seizure': ['Neurology'],
    'urine': ['Urology'],
    'kidney': ['Urology'],
    'rehab': ['Physiatry'],
    'stroke recovery': ['Physiatry'],
}


def recommend_departments(text: str) -> List[str]:
    if not text:
        return []
    text_l = text.lower()
    candidates: List[str] = []
    for kw, depts in SYMPTOM_MAP.items():
        if kw in text_l:
            candidates.extend(depts)
    if not candidates:
        # Fallback when no specific keyword matched
        candidates = ['General Medicine']
    # De-duplicate while preserving order
    seen = set()
    ordered = []
    for d in candidates:
        if d not in seen:
            seen.add(d)
            ordered.append(d)
    return ordered


def recommend_doctors(departments: Sequence[str], limit: int = 8):
    if not departments:
        return []
    qs = (
        Doctor_Information.objects.select_related('department_name', 'specialization')
        .filter(
            Q(specialization__specialization_name__in=departments) |
            Q(department_name__hospital_department_name__in=departments) |
            Q(department__in=departments)
        )
        .order_by('doctor_id')
    )
    results = []
    for d in qs[:limit]:
        results.append({
            'id': d.doctor_id,
            'name': d.name,
            'image_url': getattr(getattr(d, 'featured_image', None), 'url', ''),
            'hospital': getattr(d, 'hospital_name', ''),
            'department': (
                d.specialization.specialization_name if d.specialization else (
                    d.department_name.hospital_department_name if d.department_name else d.department
                )
            ),
            'profile_url_name': 'doctor-profile',
        })
    return results