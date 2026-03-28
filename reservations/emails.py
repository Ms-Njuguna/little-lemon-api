from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_html_email(subject, recipient_email, template_name, context):
    """Helper function to send branded HTML emails."""
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

def send_reservation_created_email(user, reservation):
    context = {
        'full_name': user.full_name,
        'date': reservation.date,
        'slot': reservation.time_slot.label,
        'guests': reservation.guests,
        'status': 'Pending'
    }
    send_html_email("Reservation Received 🍋 — Little Lemon", user.email, 'emails/reservation_created.html', context)

def send_reservation_confirmed_email(user, reservation):
    context = {
        'full_name': user.full_name,
        'date': reservation.date,
        'slot': reservation.time_slot.label,
        'guests': reservation.guests,
        'table': reservation.table.table_number
    }
    send_html_email("Reservation Confirmed ✅ — Little Lemon", user.email, 'emails/reservation_confirmed.html', context)

def send_reservation_cancelled_email(user, reservation):
    context = {
        'full_name': user.full_name,
        'date': reservation.date,
        'slot': reservation.time_slot.label
    }
    send_html_email("Reservation Cancelled — Little Lemon", user.email, 'emails/reservation_cancelled.html', context)