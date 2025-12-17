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
]