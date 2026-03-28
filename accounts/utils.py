import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


def generate_otp(length=6):
    return "".join(str(random.randint(0, 9)) for _ in range(length))


def set_verification_otp(user, minutes=10):
    otp = generate_otp(6)
    user.email_verification_code = otp
    user.email_verification_expires_at = timezone.now() + timedelta(minutes=minutes)
    user.is_active = False
    user.is_email_verified = False
    user.save(update_fields=[
        "email_verification_code",
        "email_verification_expires_at",
        "is_active",
        "is_email_verified"
    ])
    return otp


def send_verification_email(user, otp):
    subject = "Verify your email for Little Lemon"
    message = (
        f"Hi {user.full_name},\n\n"
        f"Your verification code is: {otp}\n\n"
        "This code expires in 10 minutes.\n\n"
        "— Little Lemon"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def send_welcome_email(user):
    subject = "Welcome to Little Lemon 🎉"
    message = (
        f"Hi {user.full_name},\n\n"
        "Welcome to Little Lemon! Your email has been verified successfully.\n\n"
        "You can now book tables and manage your reservations.\n\n"
        "— Little Lemon"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])