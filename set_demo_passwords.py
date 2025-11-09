import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthstack.settings')
django.setup()

from hospital.models import User

DOCTOR_USERS = [
    'aditi_doctor',
    'rafi_doctor',
    'sudarshan_doctor',
    'iqbal_doctor',
    'ismail_doctor',
]

PATIENT_USERS = [
    'soumiya_patient',
    'rajiv_patient',
]

def ensure_password(username: str, password: str, role_flag: str):
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        # Ensure role flags
        if role_flag == 'doctor':
            user.is_doctor = True
        elif role_flag == 'patient':
            user.is_patient = True
        user.is_active = True
        user.save()
        print(f"[OK] Password set for {username} -> {password}")
    except User.DoesNotExist:
        print(f"[WARN] User not found: {username}")
    except Exception as e:
        print(f"[ERROR] {username}: {str(e)}")

def main():
    print("\n[INFO] Setting demo passwords for doctors...")
    for u in DOCTOR_USERS:
        ensure_password(u, 'Doctor@123', 'doctor')

    print("\n[INFO] Setting demo passwords for patients...")
    for u in PATIENT_USERS:
        ensure_password(u, 'Patient@123', 'patient')

    print("\n[SUCCESS] Demo passwords ensured for listed users.")

if __name__ == '__main__':
    main()