from django import forms
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import EventRequest, Event, MenuItem

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



class BarleryUserCreationForm(UserCreationForm):
    """
    Custom user creation form for Barlery.
    Creates users with is_active=False by default.
    """
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'your.email@example.com'})
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '(555) 555-5555'})
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.is_active = False  # Inactive until staff activates
        if commit:
            user.save()
        return user

class EventForm(forms.ModelForm):
    """
    Form for creating and editing events.
    """
    class Meta:
        model = Event
        fields = ('title', 'date', 'start_time', 'end_time', 'description')
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Event name'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Tell us about the event...'}),
        }
        
        labels = {
            'title': 'Event Title',
            'date': 'Event Date',
            'start_time': 'Start Time',
            'end_time': 'End Time (Optional)',
            'description': 'Description',
        }
    
    def clean_date(self):
        """
        Validate that the event date is today or in the future.
        """
        from django.utils import timezone
        
        date = self.cleaned_data.get('date')
        if date:
            today = timezone.localdate()
            if date < today:
                raise forms.ValidationError("Event date must be today or a future date.")
        return date


class MenuItemForm(forms.ModelForm):
    """
    Form for creating and editing menu items.
    """
    class Meta:
        model = MenuItem
        fields = ('name', 'category', 'abv', 'description', 'price')
        
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Item name'}),
            'category': forms.Select(),
            'abv': forms.NumberInput(attrs={'placeholder': 'e.g., 5.0', 'step': '0.1'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Description (optional)'}),
            'price': forms.NumberInput(attrs={'placeholder': 'e.g., 8.00', 'step': '0.01'}),
        }
        
        labels = {
            'name': 'Item Name',
            'category': 'Category',
            'abv': 'ABV (%)',
            'description': 'Description',
            'price': 'Price ($)',
        }

class UserEditForm(forms.ModelForm):
    """
    Form for staff to edit user phone and permissions.
    """
    PERMISSION_CHOICES = [
        ('basic', 'Basic'),
        ('elevated', 'Elevated'),
    ]
    
    permission_level = forms.ChoiceField(
        choices=PERMISSION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Permissions'
    )
    
    class Meta:
        model = User
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(555) 555-5555'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial permission level based on is_staff
        if self.instance and self.instance.pk:
            self.fields['permission_level'].initial = 'elevated' if self.instance.is_staff else 'basic'