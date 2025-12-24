"""
Email sending functions for Barlery.

This module contains all email logic separated from views for better organization.
"""

from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_contact_email(name, email, subject, message):
    """
    Send a contact form submission email to staff.
    
    Args:
        name (str): Name of the person contacting
        email (str): Email address of the person contacting
        subject (str): Subject of the contact message
        message (str): Message content
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    email_subject = f"[Barlery Contact] {subject}"
    
    # Format email body with styled headers
    email_body = f"""---Contact Form Submission---

CONTACT INFORMATION:
--------------------
Name: {name}
Email: {email}

SUBJECT:
--------
{subject}

MESSAGE:
--------
{message}

---
This is an automated notification from the Barlery website.
"""
    
    try:
        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send contact email: {str(e)}", exc_info=True)
        return False


def send_venue_request_email(event_request):
    """
    Send a venue rental request notification email to staff.
    
    Args:
        event_request (EventRequest): The EventRequest model instance
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from .models import EventRequest
    
    # Subject line
    subject = f"[Barlery Venue Request] {event_request.nature} on {event_request.date.strftime('%B %d, %Y')}"
    
    # Format contact preference for display
    contact_pref_display = dict(EventRequest.CONTACT_CHOICES).get(
        event_request.contact_preference, 
        event_request.contact_preference
    )
    
    # Build the email body
    message = f"""---Venue Rental Request---

CONTACT INFORMATION:
--------------------
Name: {event_request.first_name} {event_request.last_name}
Email: {event_request.email}
Phone: {event_request.phone}
Preferred Contact Method: {contact_pref_display}
{f"Organization: {event_request.organization}" if event_request.organization else ""}

EVENT DETAILS:
-------------
Nature of Event: {event_request.nature}
Date: {event_request.date.strftime('%A, %B %d, %Y')}
Start Time: {event_request.start_time.strftime('%I:%M %p')}
End Time: {event_request.end_time.strftime('%I:%M %p')}

DESCRIPTION:
-----------
{event_request.description}

REQUEST SUBMITTED:
-----------------
{event_request.date_requested.strftime('%B %d, %Y at %I:%M %p')}

---
This is an automated notification from the Barlery website.
"""
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send venue request email: {str(e)}", exc_info=True)
        return False