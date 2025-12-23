from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone

from .forms import ContactForm, EventRequestForm
from .models import Event, WeeklyHours

def index(request):
    # Get upcoming events
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    
    hours = WeeklyHours.load()

    return render(request, 'barlery/index.html', {
        'upcoming_events': upcoming_events, "hours": hours
    })

def about(request):
    return render(request, "barlery/about.html")

def menu(request):
    from .models import MenuItem
    # Get menu items grouped by category
    beer_items = MenuItem.objects.filter(category=MenuItem.CATEGORY_BEER).order_by('name')
    wine_items = MenuItem.objects.filter(category=MenuItem.CATEGORY_WINE).order_by('name')
    spirit_items = MenuItem.objects.filter(category=MenuItem.CATEGORY_SPIRIT).order_by('name')
    food_items = MenuItem.objects.filter(category=MenuItem.CATEGORY_FOOD).order_by('name')
    non_alcoholic_items = MenuItem.objects.filter(category=MenuItem.CATEGORY_NON_ALCOHOLIC).order_by('name')
    
    # Also pass all items for the "no menu" check
    menu_items = MenuItem.objects.all()
    
    return render(request, "barlery/menu.html", {
        "menu_items": menu_items,
        "beer_items": beer_items,
        "wine_items": wine_items,
        "spirit_items": spirit_items,
        "food_items": food_items,
        "non_alcoholic_items": non_alcoholic_items,
    })

def calendar(request):
    # Get all upcoming events, ordered by date and time
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date', 'start_time')
    return render(request, "barlery/calendar.html", {"upcoming_events": upcoming_events})

def venue(request):
    if request.method == "POST":
        form = EventRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thanks! Your event request has been submitted. We’ll be in touch soon."
            )
            return redirect("barlery:venue")
    else:
        form = EventRequestForm()

    return render(
        request,
        "barlery/venue.html",
        {"form": form}
    )

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            full_subject = f"[Barlery Contact] {subject}"
            full_message = f"From: {name} <{email}>{message}"

            send_mail(
                subject=full_subject,
                message=full_message,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Thanks! We received your message. We'll be in touch soon.")
            return redirect("barlery:contact")
    else:
        form = ContactForm()

    hours = WeeklyHours.load()
    return render(request, "barlery/contact.html", {"form": form, "hours": hours})

def privacy(request):
    return render(request, "barlery/privacy.html")

def successful_logout(request):
    return render(request, "barlery/index.html")