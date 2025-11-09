import os
import sys
import random
import argparse
from pathlib import Path

import django

# Ensure project package is importable when running from repo root
PROJECT_DIR = Path(__file__).resolve().parent / "HealthStack-System-main"
if PROJECT_DIR.exists():
    sys.path.insert(0, str(PROJECT_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthstack.settings")
django.setup()

from doctor.models import Doctor_Information, Education
from hospital_admin.models import hospital_department, specialization
from hospital.models import Hospital_Information


# Seeded randomness for reproducible runs; change or remove for different results
random.seed(42)


# Canonical clinical categories we’ll assign
CATEGORIES = [
    {"key": "Cardiology", "designation": "Cardiologist", "dept_choice": "Cardiologists"},
    {"key": "Neurology", "designation": "Neurologist", "dept_choice": "Neurologists"},
    {"key": "Dentistry", "designation": "Dentist", "dept_choice": None},
    {"key": "Orthopedics", "designation": "Orthopedic Surgeon", "dept_choice": None},
    {"key": "Dermatology", "designation": "Dermatologist", "dept_choice": "Dermatologists"},
    {"key": "Pediatrics", "designation": "Pediatrician", "dept_choice": "Pediatricians"},
    {"key": "Physiatry", "designation": "Physiatrist", "dept_choice": "Physiatrists"},
    {"key": "General Medicine", "designation": "General Practitioner", "dept_choice": None},
    {"key": "Urology", "designation": "Urologist", "dept_choice": None},
]

# Optional bias profiles for category distribution
CATEGORY_BIAS_PROFILES = {
    "default": {
        "Cardiology": 2,
        "Neurology": 2,
        "General Medicine": 2,
        "Dermatology": 1,
        "Dentistry": 1,
        "Orthopedics": 1,
        "Pediatrics": 1,
        "Physiatry": 1,
        "Urology": 1,
    },
    "cardio_heavy": {
        "Cardiology": 3,
        "Neurology": 2,
        "General Medicine": 2,
        "Dermatology": 1,
        "Dentistry": 1,
        "Orthopedics": 1,
        "Pediatrics": 1,
        "Physiatry": 1,
        "Urology": 1,
    },
}


# Reasonable fee ranges
CONSULTATION_FEES = [300, 400, 500, 600, 700, 800]
REPORT_FEES = [150, 200, 250, 300, 350, 400]


VISITING_SLOTS = [
    "Mon–Fri 09:00–12:00",
    "Mon–Fri 10:00–13:00",
    "Mon–Sat 11:00–14:00",
    "Tue–Sun 16:00–19:00",
    "Mon–Fri 17:00–20:00",
]


# Degrees by category for realistic profiles
DEGREES_BY_CATEGORY = {
    "Cardiology": ["MBBS", "MD - General Medicine", "DNB - Cardiology"],
    "Neurology": ["MBBS", "MD - General Medicine", "DM - Neurology"],
    "Dentistry": ["BDS", "MDS - Oral & Maxillofacial Surgery"],
    "Orthopedics": ["MBBS", "MS - Orthopaedics", "M.Ch - Orthopaedics"],
    "Dermatology": ["MBBS", "MD - Dermatology, Venereology & Leprosy"],
    "Pediatrics": ["MBBS", "MD - Pediatrics"],
    "Physiatry": ["MBBS", "MD - Physical Medicine and Rehabilitation"],
    "General Medicine": ["MBBS", "MD - General Medicine"],
    "Urology": ["MBBS", "MS - General Surgery", "MCh - Urology"],
}

INSTITUTES = [
    "AIIMS Delhi",
    "CMC Vellore",
    "PGI Chandigarh",
    "NIMHANS Bengaluru",
    "KGMU Lucknow",
    "MAMC Delhi",
    "JIPMER Puducherry",
]


def pick_category():
    return random.choice(CATEGORIES)


def pick_hospital():
    hospitals = list(Hospital_Information.objects.all())
    return random.choice(hospitals) if hospitals else None


def ensure_department(hospital, category_key):
    if not hospital:
        return None
    dept, _ = hospital_department.objects.get_or_create(
        hospital=hospital,
        hospital_department_name=category_key,
    )
    return dept


def ensure_specialization(hospital, category_key):
    if not hospital:
        return None
    spec, _ = specialization.objects.get_or_create(
        hospital=hospital,
        specialization_name=category_key,
    )
    return spec


def _build_category_order(total, bias_profile):
    # Build a weighted base list from bias profile
    weights = CATEGORY_BIAS_PROFILES.get(bias_profile, CATEGORY_BIAS_PROFILES["default"])
    weighted = []
    key_to_cat = {c["key"]: c for c in CATEGORIES}
    for key, w in weights.items():
        cat = key_to_cat.get(key)
        if not cat:
            continue
        weighted.extend([cat] * max(1, int(w)))

    random.shuffle(weighted)
    if not weighted:
        weighted = CATEGORIES.copy()
        random.shuffle(weighted)

    order = []
    prev_key = None
    i = 0
    while len(order) < total:
        cand = weighted[i % len(weighted)]
        if prev_key and cand["key"] == prev_key:
            # try next candidate to avoid adjacency repeat
            cand = weighted[(i + 1) % len(weighted)]
        order.append(cand)
        prev_key = cand["key"]
        i += 1
    return order


def assign_random_details():
    total = 0
    updated = 0

    doctors = list(Doctor_Information.objects.all())
    total = len(doctors)

    # Parse overwrite and fine-tuning behavior
    parser = argparse.ArgumentParser(description="Assign random doctor details")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing degrees and categories")
    parser.add_argument("--bias", choices=list(CATEGORY_BIAS_PROFILES.keys()), default="cardio_heavy", help="Category bias profile")
    parser.add_argument("--degree-count", type=int, default=2, help="Exact number of degrees to assign")
    parser.add_argument("--max-degree-count", type=int, default=None, help="Max number of degrees when not using exact count")
    parser.add_argument("--year-min", type=int, default=2008, help="Minimum completion year")
    parser.add_argument("--year-max", type=int, default=2021, help="Maximum completion year")
    args, _ = parser.parse_known_args()

    category_order = _build_category_order(total, args.bias)

    for idx, doc in enumerate(doctors):
        cat = category_order[idx]

        # Pick or keep hospital
        hospital = doc.hospital_name or pick_hospital()

        # Ensure department and specialization tied to hospital
        dept_obj = ensure_department(hospital, cat["key"]) if hospital else None
        spec_obj = ensure_specialization(hospital, cat["key"]) if hospital else None

        # Assign fields
        if args.overwrite:
            doc.hospital_name = hospital or doc.hospital_name
            doc.department_name = dept_obj or doc.department_name
            doc.specialization = spec_obj or doc.specialization
            doc.designation = cat["designation"]
            if cat["dept_choice"]:
                doc.department = cat["dept_choice"]
            doc.consultation_fee = random.choice(CONSULTATION_FEES)
            doc.report_fee = random.choice(REPORT_FEES)
            doc.visiting_hour = random.choice(VISITING_SLOTS)
        else:
            # Only fill missing values
            if not doc.hospital_name:
                doc.hospital_name = hospital
            if not doc.department_name and dept_obj:
                doc.department_name = dept_obj
            if not doc.specialization and spec_obj:
                doc.specialization = spec_obj
            if not doc.designation:
                doc.designation = cat["designation"]
            if not doc.department and cat["dept_choice"]:
                doc.department = cat["dept_choice"]
            if not doc.consultation_fee:
                doc.consultation_fee = random.choice(CONSULTATION_FEES)
            if not doc.report_fee:
                doc.report_fee = random.choice(REPORT_FEES)
            if not doc.visiting_hour:
                doc.visiting_hour = random.choice(VISITING_SLOTS)

        doc.save()

        # Add random degrees
        existing_edu_qs = Education.objects.filter(doctor=doc)
        if args.overwrite and existing_edu_qs.exists():
            existing_edu_qs.delete()
        if args.overwrite or not existing_edu_qs.exists():
            degree_pool = DEGREES_BY_CATEGORY.get(cat["key"], ["MBBS"])
            if args.max_degree_count is not None and args.degree_count is None:
                num_degrees = random.randint(1, max(1, args.max_degree_count))
            else:
                num_degrees = max(1, args.degree_count)
            chosen = random.sample(degree_pool, k=min(num_degrees, len(degree_pool)))
            for deg in chosen:
                edu = Education(doctor=doc)
                edu.degree = deg
                edu.institute = random.choice(INSTITUTES)
                edu.year_of_completion = str(random.randint(args.year_min, args.year_max))
                edu.save()
        updated += 1

    print(f"Processed {total} doctors; updated {updated} with random details.")


if __name__ == "__main__":
    assign_random_details()