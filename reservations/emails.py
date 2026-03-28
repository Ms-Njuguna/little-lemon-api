# reservations/emails.py
from django.core.mail import send_mail
from django.conf import settings

def send_reservation_created_email(user, reservation):
    """Sends email when reservation is created (pending)."""
    subject = "Reservation received (Pending) — Little Lemon"
    message = (
        f"Hi {user.full_name},\n\n"
        f"We received your reservation for {reservation.date} "
        f"({reservation.time_slot.label}). Status: {reservation.status}.\n\n"
        "— Little Lemon"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

def send_reservation_confirmed_email(user, reservation):
    """Sends email when reservation is confirmed."""
    subject = "Reservation confirmed ✅ — Little Lemon"
    message = (
        f"Hi {user.full_name},\n\n"
        f"Your reservation for {reservation.date} ({reservation.time_slot.label}) is confirmed.\n\n"
        "— Little Lemon"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

def send_reservation_cancelled_email(user, reservation):
    """Sends email when reservation is cancelled."""
    subject = "Reservation cancelled — Little Lemon"
    message = (
        f"Hi {user.full_name},\n\n"
        f"Your reservation for {reservation.date} ({reservation.time_slot.label}) was cancelled.\n\n"
        "— Little Lemon"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)