from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, MenuItem, Event, EventRequest

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "phone", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name", "phone")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "phone", "password1", "password2"),
        }),
    )

    readonly_fields = ("date_joined",)


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
class EventRequestAdmin(admin.ModelAdmin):
    # Make "nature" the first (linked) column
    list_display = ("nature", "date_requested", "date", "start_time", "end_time", "first_name", "last_name", "contact_preference", "email", "phone")
    list_display_links = ("nature",)

    # Sort by most recent request first
    ordering = ("-date_requested",)

    # Helpful extras (optional but nice)
    list_filter = ("date_requested", "date")
    search_fields = ("nature", "organization", "first_name", "last_name", "email", "phone", "description")
    readonly_fields = ("date_requested",)