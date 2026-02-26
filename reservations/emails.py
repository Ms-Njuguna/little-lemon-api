from django.core.mail import send_mail
from django.conf import settings

def send_reservation_created_email(user, reservation):
    send_mail(
        "Reservation received (Pending) — Little Lemon",
        f"Hi {user.full_name},\n\n"
        f"We received your reservation for {reservation.date} "
        f"({reservation.time_slot.label}). Status: {reservation.status}.\n\n"
        "— Little Lemon",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )

def send_reservation_confirmed_email(user, reservation):
    send_mail(
        "Reservation confirmed ✅ — Little Lemon",
        f"Hi {user.full_name},\n\n"
        f"Your reservation for {reservation.date} ({reservation.time_slot.label}) is confirmed.\n\n"
        "— Little Lemon",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )

def send_reservation_cancelled_email(user, reservation):
    send_mail(
        "Reservation cancelled — Little Lemon",
        f"Hi {user.full_name},\n\n"
        f"Your reservation for {reservation.date} ({reservation.time_slot.label}) was cancelled.\n\n"
        "— Little Lemon",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )