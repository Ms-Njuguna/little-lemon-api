import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
        "is_email_verified"
    ])
    return otp

def send_html_email(subject, recipient_email, template_name, context):
    """Helper to send branded HTML emails from accounts."""
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_verification_email(user, otp):
    """Sends a branded 6-digit verification code email."""
    context = {
        'full_name': user.full_name,
        'otp': otp,
        'expires': 10
    }
    send_html_email(
        "Verify your email — Little Lemon",
        user.email,
        'emails/verify_email.html',
        context
    )

def send_welcome_email(user):
    """Sends a branded welcome email."""
    context = {
        'full_name': user.full_name,
    }
    send_html_email(
        "Welcome to Little Lemon! 🎉",
        user.email,
        'emails/welcome.html',
        context
    )