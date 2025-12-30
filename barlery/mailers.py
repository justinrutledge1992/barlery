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
    email_subject = f"[Contact Form] {subject}"
    
    # Format email body with styled headers
    email_body = f"""New Contact Form Submission

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
    from django.utils import timezone
    
    # Convert timezone-aware datetimes to local timezone
    local_tz = timezone.get_current_timezone()
    date_requested_local = timezone.localtime(event_request.date_requested, local_tz)
    
    # Subject line
    subject = f"[Venue Request] {event_request.nature} on {event_request.date.strftime('%B %d, %Y')}"
    
    # Format contact preference for display
    contact_pref_display = dict(EventRequest.CONTACT_CHOICES).get(
        event_request.contact_preference, 
        event_request.contact_preference
    )
    
    # Build the email body
    message = f"""New Venue Rental Request Submitted

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
Start Time: {event_request.start_time.strftime('%I:%M %p')} ET
End Time: {event_request.end_time.strftime('%I:%M %p')} ET

DESCRIPTION:
-----------
{event_request.description}

REQUEST SUBMITTED:
-----------------
{date_requested_local.strftime('%B %d, %Y at %I:%M %p')} ET

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


def send_new_user_email(user):
    """
    Send notification email to staff when a new user account is created.
    
    Args:
        user: User model instance (newly created, inactive)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from django.utils import timezone
    
    # Convert timezone-aware datetime to local timezone
    local_tz = timezone.get_current_timezone()
    date_joined_local = timezone.localtime(user.date_joined, local_tz)
    
    subject = f"[Barlery] New User Account Created: {user.first_name} {user.last_name}"
    
    message = f"""New User Account Created

A new user has requested an account on the Barlery website.

USER INFORMATION:
-----------------
Name: {user.first_name} {user.last_name}
Email: {user.email}
Date Requested: {date_joined_local.strftime('%B %d, %Y at %I:%M %p')} ET

NEXT STEPS:
-----------
This account is currently INACTIVE and pending approval.

To activate this account, please visit:
{settings.SITE_URL}/accounts/management

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
        logger.error(f"Failed to send new user email: {str(e)}", exc_info=True)
        return False


def send_user_activation_email(user):
    """
    Send notification email to staff when a user account is activated.
    
    Args:
        user: User model instance (newly activated)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    from django.utils import timezone
    
    # Convert timezone-aware datetime to local timezone
    local_tz = timezone.get_current_timezone()
    date_joined_local = timezone.localtime(user.date_joined, local_tz)
    
    subject = f"[Barlery] User Account Activated: {user.first_name} {user.last_name}"
    
    message = f"""User Account Activated

A user account has been activated on the Barlery website.

USER INFORMATION:
-----------------
Name: {user.first_name} {user.last_name}
Email: {user.email}
Account Created: {date_joined_local.strftime('%B %d, %Y at %I:%M %p')} ET
Activated: Just now

STATUS:
-------
This user can now log in to the Barlery system.

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
        logger.error(f"Failed to send user activation email: {str(e)}", exc_info=True)
        return False