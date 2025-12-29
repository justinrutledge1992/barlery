from django.urls import path
from . import views

app_name = "barlery"

urlpatterns = [
    # Home Page:
    path("", views.index, name="index"),

    # Other Static Pages:
    path("about", views.about, name="about"),
    path("calendar", views.calendar, name="calendar"),
    path("event/details/<int:event_id>/", views.event_details, name="event_details"),
    path("event/create/", views.event_create, name="event_create"),
    path("event/edit/<int:event_id>/", views.event_edit, name="event_edit"),
    path("event/delete/<int:event_id>/", views.event_delete, name="event_delete"),
    path("menu_item/create/", views.menu_item_create, name="menu_item_create"),
    path("menu_item/edit/<int:item_id>/", views.menu_item_edit, name="menu_item_edit"),
    path("menu_item/delete/<int:item_id>/", views.menu_item_delete, name="menu_item_delete"),
    path("contact", views.contact, name="contact"),
    path("menu", views.menu, name="menu"),
    path("venue", views.venue, name="venue"),
    path("privacy", views.privacy, name="privacy"),
    path("success", views.success, name="success"),
    path("hours/edit/", views.hours_edit, name="hours_edit"),

    # User Creation & Activation:
    path("accounts/create", views.user_create, name="user_create"),
    path("accounts/activate/<int:user_id>/", views.activate_user, name="activate_user"),
    path("accounts/deactivate/<int:user_id>/", views.deactivate_user, name="deactivate_user"),
    path("accounts/edit/<int:user_id>/", views.edit_user, name="edit_user"),
    
    # Accounts (Custom):
    path("accounts/login/", views.custom_login, name="login"),
    path("accounts/logout/", views.custom_logout, name="logout"),
    path("accounts/management/", views.account_management, name="account_management"),
]