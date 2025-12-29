from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from datetime import datetime, time, timedelta
from django.db import models
from django.utils import timezone
from django.forms import ValidationError
import re

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        if not first_name:
            raise ValueError("First name is required.")
        if not last_name:
            raise ValueError("Last name is required.")
        if not phone:
            raise ValueError("Phone number is required.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, first_name, last_name, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"
    

# Singleton model for open hours
class WeeklyHours(models.Model):
    # Force a single-row table by pinning the PK to 1
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)

    monday_open = models.TimeField(null=True, blank=True)
    monday_close = models.TimeField(null=True, blank=True)
    tuesday_open = models.TimeField(null=True, blank=True)
    tuesday_close = models.TimeField(null=True, blank=True)
    wednesday_open = models.TimeField(null=True, blank=True)
    wednesday_close = models.TimeField(null=True, blank=True)
    thursday_open = models.TimeField(null=True, blank=True)
    thursday_close = models.TimeField(null=True, blank=True)
    friday_open = models.TimeField(null=True, blank=True)
    friday_close = models.TimeField(null=True, blank=True)
    saturday_open = models.TimeField(null=True, blank=True)
    saturday_close = models.TimeField(null=True, blank=True)
    sunday_open = models.TimeField(null=True, blank=True)
    sunday_close = models.TimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Always overwrite the singleton row
        self.id = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Optional: prevent deleting the singleton (keeps table stable)
        return

    @classmethod
    def load(cls):
        # Convenience accessor: always returns “the” WeeklyHours record
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
    
    from django.db import models

    class Meta:
        verbose_name_plural = "Weekly hours"
        # Optional: You can also set the singular name explicitly
        verbose_name = "Weekly hours"



class MenuItem(models.Model):
    # Category choices
    CATEGORY_FOOD = 'food'
    CATEGORY_BEER = 'beer'
    CATEGORY_WINE = 'wine'
    CATEGORY_SPIRIT = 'spirit'
    CATEGORY_NON_ALCOHOLIC = 'non-alcoholic'
    
    CATEGORY_CHOICES = [
        (CATEGORY_FOOD, 'Food'),
        (CATEGORY_BEER, 'Beer'),
        (CATEGORY_WINE, 'Wine'),
        (CATEGORY_SPIRIT, 'Spirit'),
        (CATEGORY_NON_ALCOHOLIC, 'Non-Alcoholic'),
    ]
    
    name = models.CharField("Product Name", max_length=255)
    category = models.CharField(
        "Category",
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_BEER,
    )
    abv = models.DecimalField("ABV (%)", max_digits=3, decimal_places=1, null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField("Price ($)", max_digits=6, decimal_places=2, null=True, blank=True)
    last_updated = models.DateTimeField() # represents when this item was last added/updated

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='events/',
        null=True,
        blank=True,
        help_text='Event promotional image'
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date", "start_time"]

    def clean(self):
        if self.end_time and self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    def has_valid_image(self):
        """
        Check if event has a valid image file in storage.
        
        Returns:
            bool: True if image exists in storage, False otherwise
        """
        if not self.image:
            return False
        
        try:
            # Check if the file exists in storage (works for both local and R2)
            return self.image.storage.exists(self.image.name)
        except Exception:
            # If there's any error checking (permissions, network, etc.), assume it doesn't exist
            return False

    def save(self, *args, **kwargs):
        """Override save to delete old image when updating."""
        if self.pk:  # Only for existing objects (updates)
            try:
                old_event = Event.objects.get(pk=self.pk)
                # If image has changed and there was an old image, delete it
                if old_event.image and old_event.image != self.image:
                    if old_event.image.storage.exists(old_event.image.name):
                        old_event.image.storage.delete(old_event.image.name)
            except Event.DoesNotExist:
                pass  # New object, nothing to delete
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Override delete to remove image from storage."""
        # Delete the image file before deleting the database record
        if self.image:
            if self.image.storage.exists(self.image.name):
                self.image.storage.delete(self.image.name)
        
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.date})"


class EventRequest(models.Model):
    CONTACT_EMAIL = "email"
    CONTACT_PHONE = "phone"
    CONTACT_TEXT = "text"

    CONTACT_CHOICES = [
        (CONTACT_EMAIL, "Email"),
        (CONTACT_PHONE, "Phone"),
        (CONTACT_TEXT, "Text"),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    contact_preference = models.CharField(
        "Contact Preference",
        max_length=10,
        choices=CONTACT_CHOICES,
    )

    organization = models.CharField(
        max_length=255,
        blank=True
    )

    nature = models.CharField("Nature of Event", max_length=255)
    date = models.DateField("Event Date",)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()

    date_requested = models.DateTimeField("Request Submitted On",auto_now_add=True)

    def clean(self):
        super().clean()

        errors = {}  # field_name -> list[str] or str

        # --- Date must be today or later ---
        if self.date:
            today = timezone.localdate()
            if self.date < today:
                errors.setdefault("date", []).append("Please choose a future date.")

        # --- Phone validation (US 10-digit, allows punctuation) ---
        if self.phone:
            digits = re.sub(r"\D", "", self.phone)
            if len(digits) == 11 and digits.startswith("1"):
                digits = digits[1:]
            if len(digits) != 10:
                errors.setdefault("phone", []).append("Enter a valid US phone number (10 digits).")

        # --- Time + duration validation ---
        if self.start_time and self.end_time:
            if self.date:
                date = self.date
            else:
                date = timezone.now()

            start_dt = datetime.combine(date, self.start_time)
            end_dt = datetime.combine(date, self.end_time)

            # Treat any end time before 3:00 AM as next-day
            if self.end_time < time(3, 0):
                end_dt += timedelta(days=1)

            if end_dt - start_dt > timedelta(hours=24):
                # non-field error (shows at top of form via form.non_field_errors)
                errors.setdefault("end_time", []).append("Event duration cannot exceed 24 hours.")

            if end_dt <= start_dt:
                errors.setdefault("end_time", []).append("End time must be after start time.")

        # Raise once, after all checks
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.first_name} {self.last_name} – {self.date}"