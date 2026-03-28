# accounts/utils.py
import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

def generate_otp(length=6):
    """Generates a numeric OTP code."""
    return "".join(str(random.randint(0, 9)) for _ in range(length))

def set_verification_otp(user, minutes=10):
    """Sets OTP and expiry time for email verification."""
    otp = generate_otp()
    user.email_verification_code = otp
    user.email_verification_expires_at = timezone.now() + timedelta(minutes=minutes)
    user.is_active = False
    user.is_email_verified = False
    user.save(update_fields=[
        "email_verification_code",
        "email_verification_expires_at",
        "is_active",
        "is_email_verified",
    ])
    return otp

def send_verification_email(user, otp):
    """Sends a 6-digit verification code to the user's email."""
    subject = "Verify your email — Little Lemon"
    message = (
        f"Hi {user.full_name},\n\n"
        f"Thank you for signing up! Your verification code is: {otp}\n\n"
        "Please enter this code in the app to verify your email.\n\n"
        "This code expires in 10 minutes.\n\n"
        "— Little Lemon"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def send_welcome_email(user):
    """Sends a welcome email after successful email verification."""
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