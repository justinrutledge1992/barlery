from django.db import models
from django.forms import ValidationError
from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    abv = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
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
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date", "start_time"]

    def clean(self):
        if self.end_time and self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    def __str__(self):
        return f"{self.title} ({self.date})"


class EventRequest(models.Model):
    CONTACT_PHONE = "phone"
    CONTACT_EMAIL = "email"
    CONTACT_TEXT = "text"

    CONTACT_CHOICES = [
        (CONTACT_PHONE, "Phone"),
        (CONTACT_EMAIL, "Email"),
        (CONTACT_TEXT, "Text"),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    contact_preference = models.CharField(
        "Preferred Contact Method",
        max_length=10,
        choices=CONTACT_CHOICES,
    )

    organization = models.CharField(
        max_length=255,
        blank=True
    )

    nature = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()

    booked = models.BooleanField(default=False)

    date_requested = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    def __str__(self):
        return f"{self.first_name} {self.last_name} – {self.date}"
