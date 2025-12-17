from django.contrib import admin
from .models import MenuItem, Event, EventRequest

@admin.register(MenuItem)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "abv", "price")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("last_updated",)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "start_time", "end_time")
    list_filter = ("date",)
    search_fields = ("title", "description")
    ordering = ("date", "start_time")
    readonly_fields = ("last_updated",)

@admin.register(EventRequest)
class InquiryAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "date",
        "start_time",
        "contact_preference",
        "booked",
    )
    list_filter = ("booked", "contact_preference", "date")
    search_fields = ("first_name", "last_name", "email", "organization")
    ordering = ("-date", "start_time")
    readonly_fields = ("date_requested",)