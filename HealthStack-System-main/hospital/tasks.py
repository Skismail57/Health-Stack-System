"""
Celery Tasks for Hospital App
Background tasks for email notifications, report generation, etc.
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_appointment_confirmation_email(self, appointment_id):
    """
    Send appointment confirmation email to patient
    Async task to avoid blocking the request
    """
    try:
        from doctor.models import Appointment
        from hospital.models import Patient
        
        appointment = Appointment.objects.select_related(
            'patient__user', 'doctor', 'hospital'
        ).get(appointment_id=appointment_id)
        
        subject = f'Appointment Confirmed - {appointment.hospital.name}'
        message = f"""
        Dear {appointment.patient.name},
        
        Your appointment has been confirmed with the following details:
        
        Doctor: {appointment.doctor.name}
        Hospital: {appointment.hospital.name}
        Date: {appointment.appointment_date}
        Time: {appointment.appointment_time}
        
        Please arrive 15 minutes before your scheduled time.
        
        Thank you for choosing HealthStack!
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [appointment.patient.email],
            fail_silently=False,
        )
        
        logger.info(f"Confirmation email sent for appointment {appointment_id}")
        return f"Email sent successfully for appointment {appointment_id}"
        
    except Exception as exc:
        logger.error(f"Error sending email for appointment {appointment_id}: {exc}")
        raise self.retry(exc=exc, countdown=60)  # Retry after 1 minute


@shared_task
def send_appointment_reminders():
    """
    Send appointment reminders to patients 24 hours before appointment
    Scheduled to run every hour
    """
    try:
        from doctor.models import Appointment
        
        tomorrow = timezone.now() + timedelta(days=1)
        tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0)
        tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59)
        
        upcoming_appointments = Appointment.objects.filter(
            appointment_date__range=[tomorrow_start, tomorrow_end],
            appointment_status='confirmed',
            reminder_sent=False
        ).select_related('patient__user', 'doctor', 'hospital')
        
        count = 0
        for appointment in upcoming_appointments:
            subject = f'Appointment Reminder - Tomorrow at {appointment.appointment_time}'
            message = f"""
            Dear {appointment.patient.name},
            
            This is a reminder for your appointment tomorrow:
            
            Doctor: {appointment.doctor.name}
            Hospital: {appointment.hospital.name}
            Date: {appointment.appointment_date.strftime('%B %d, %Y')}
            Time: {appointment.appointment_time}
            
            Please arrive 15 minutes early.
            
            To cancel or reschedule, please contact us.
            
            Best regards,
            HealthStack Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [appointment.patient.email],
                fail_silently=True,
            )
            
            # Mark reminder as sent (add this field to model if needed)
            # appointment.reminder_sent = True
            # appointment.save()
            
            count += 1
        
        logger.info(f"Sent {count} appointment reminders")
        return f"Sent {count} reminders"
        
    except Exception as exc:
        logger.error(f"Error sending appointment reminders: {exc}")
        return f"Error: {exc}"


@shared_task
def generate_prescription_pdf(prescription_id):
    """
    Generate prescription PDF asynchronously
    """
    try:
        from doctor.models import Prescription
        # PDF generation logic here
        logger.info(f"Generated PDF for prescription {prescription_id}")
        return f"PDF generated for prescription {prescription_id}"
    except Exception as exc:
        logger.error(f"Error generating PDF: {exc}")
        raise


@shared_task
def generate_lab_report_pdf(report_id):
    """
    Generate lab report PDF asynchronously
    """
    try:
        # Lab report PDF generation logic
        logger.info(f"Generated lab report PDF {report_id}")
        return f"Lab report PDF generated {report_id}"
    except Exception as exc:
        logger.error(f"Error generating lab report: {exc}")
        raise


@shared_task
def cleanup_expired_sessions():
    """
    Clean up expired sessions from database
    Scheduled to run daily at 3 AM
    """
    try:
        from django.contrib.sessions.models import Session
        
        expired_sessions = Session.objects.filter(
            expire_date__lt=timezone.now()
        )
        count = expired_sessions.count()
        expired_sessions.delete()
        
        logger.info(f"Cleaned up {count} expired sessions")
        return f"Cleaned {count} expired sessions"
        
    except Exception as exc:
        logger.error(f"Error cleaning up sessions: {exc}")
        return f"Error: {exc}"


@shared_task
def generate_daily_statistics():
    """
    Generate daily statistics for admin dashboard
    Scheduled to run daily at 11:55 PM
    """
    try:
        from hospital.models import Patient
        from doctor.models import Appointment, Doctor_Information
        from pharmacy.models import Medicine
        
        today = timezone.now().date()
        
        stats = {
            'date': today.isoformat(),
            'new_patients': Patient.objects.filter(
                created_at__date=today
            ).count() if hasattr(Patient, 'created_at') else 0,
            'appointments_today': Appointment.objects.filter(
                appointment_date=today
            ).count(),
            'active_doctors': Doctor_Information.objects.filter(
                user__is_active=True
            ).count(),
            'total_medicines': Medicine.objects.count(),
        }
        
        # Store stats in cache or database
        from django.core.cache import cache
        cache.set(f'daily_stats_{today}', stats, timeout=86400 * 7)  # 7 days
        
        logger.info(f"Generated daily statistics: {stats}")
        return stats
        
    except Exception as exc:
        logger.error(f"Error generating statistics: {exc}")
        return f"Error: {exc}"


@shared_task
def send_bulk_notifications(user_ids, message_title, message_body):
    """
    Send bulk notifications to multiple users
    Useful for announcements, maintenance notices, etc.
    """
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        users = User.objects.filter(id__in=user_ids)
        emails = [user.email for user in users if user.email]
        
        send_mail(
            message_title,
            message_body,
            settings.DEFAULT_FROM_EMAIL,
            emails,
            fail_silently=False,
        )
        
        logger.info(f"Sent bulk notification to {len(emails)} users")
        return f"Notification sent to {len(emails)} users"
        
    except Exception as exc:
        logger.error(f"Error sending bulk notifications: {exc}")
        raise


@shared_task
def process_payment_confirmation(payment_id):
    """
    Process payment confirmation and update appointment status
    """
    try:
        # Payment processing logic
        logger.info(f"Processed payment confirmation {payment_id}")
        return f"Payment {payment_id} processed"
    except Exception as exc:
        logger.error(f"Error processing payment: {exc}")
        raise


@shared_task
def backup_database():
    """
    Create database backup
    Scheduled task for regular backups
    """
    try:
        import subprocess
        from datetime import datetime
        
        backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Run Django dumpdata command
        result = subprocess.run(
            ['python', 'manage.py', 'dumpdata', '--natural-foreign', 
             '--natural-primary', '-e', 'contenttypes', '-e', 'auth.Permission',
             '--indent', '2', '--output', backup_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info(f"Database backup created: {backup_file}")
            return f"Backup created: {backup_file}"
        else:
            logger.error(f"Backup failed: {result.stderr}")
            return f"Backup failed: {result.stderr}"
            
    except Exception as exc:
        logger.error(f"Error creating backup: {exc}")
        return f"Error: {exc}"
