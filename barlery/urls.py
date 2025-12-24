from django.urls import path
from . import views

app_name = "barlery"

urlpatterns = [
    # Home Page:
    path("", views.index, name="index"),

    # Other Static Pages:
    path("about", views.about, name="about"),
    path("calendar", views.calendar, name="calendar"),
    path("contact", views.contact, name="contact"),
    path("menu", views.menu, name="menu"),
    path("venue", views.venue, name="venue"),
    path("privacy", views.privacy, name="privacy"),
    path("success", views.success, name="success"),

    # User Creation & Activation:
    path("accounts/create", views.user_create, name="user_create"),
    path("accounts/activate/<int:user_id>/", views.activate_user, name="activate_user"),
    path("accounts/deactivate/<int:user_id>/", views.deactivate_user, name="deactivate_user"),
    
    # Accounts (Custom):
    path("accounts/login/", views.custom_login, name="login"),
    path("accounts/logout/", views.custom_logout, name="logout"),
    path("accounts/management/", views.account_management, name="account_management"),
]