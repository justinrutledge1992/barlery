from django import forms
from django import forms
from django.core.exceptions import ValidationError
from .models import EventRequest

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Your name"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"})
    )
    subject = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Subject"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6, "placeholder": "How can we help?"})
    )


class EventRequestForm(forms.ModelForm):
    class Meta:
        model = EventRequest
        # exclude fields users should never set directly
        exclude = ["booked", "date_requested"]

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "(555) 555-5555"}),

            "organization": forms.TextInput(attrs={"placeholder": "Optional"}),
            "nature": forms.TextInput(attrs={"placeholder": "e.g., Performance, Private Party, etc."}),

            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),

            "description": forms.Textarea(attrs={"rows": 6, "placeholder": "Tell us about the event..."}),
        }

        error_messages = {
            "first_name": {"required": "This field is required."},
            "last_name": {"required": "This field is required."},
            "email": {"required": "This field is required."},
            "date": {"required": "This field select a date."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove the "---------" option from contact_preference
        self.fields["contact_preference"].choices = EventRequest.CONTACT_CHOICES

        # Default to Email
        self.fields["contact_preference"].initial = EventRequest.CONTACT_EMAIL
