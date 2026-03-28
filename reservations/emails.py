from django.core.mail import send_mail
from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user, code):
    """
    Sends a 6-digit verification code to the user's email
    after signup.
    """
    subject = "Verify your email — Little Lemon"
    message = (
        f"Hi {user.full_name},\n\n"
        f"Thank you for signing up! Your verification code is: {code}\n\n"
        "Please enter this code in the app to verify your email.\n\n"
        "— Little Lemon"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,  # Important: raises errors if email fails
    )

def send_welcome_email(user):
    """
    Sends a welcome email after successful email verification.
    """
    subject = "Welcome to Little Lemon! 🎉"
    message = (
        f"Hi {user.full_name},\n\n"
        "Your email has been successfully verified. "
        "You can now log in and enjoy our app!\n\n"
        "— Little Lemon"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
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