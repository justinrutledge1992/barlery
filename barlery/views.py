from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone

from .forms import ContactForm, EventRequestForm
from .models import Event, WeeklyHours, EventRequest
from .mailers import send_contact_email, send_venue_request_email

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
    from django.http import JsonResponse
    from django.template.loader import render_to_string
    
    # Get page number from query params (default to 1)
    page = int(request.GET.get('page', 1))
    events_per_page = 9  # Show 9 events per page (3 rows of 3)
    
    # Get all upcoming events, ordered by date and time
    all_events = Event.objects.filter(date__gte=timezone.now()).order_by('date', 'start_time')
    
    # Calculate pagination
    start_idx = (page - 1) * events_per_page
    end_idx = start_idx + events_per_page
    
    events_page = all_events[start_idx:end_idx]
    has_more = end_idx < all_events.count()
    
    # If it's an AJAX request, return JSON with HTML
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        events_html = render_to_string('barlery/_event_cards_list.html', {
            'events': events_page
        })
        
        return JsonResponse({
            'html': events_html,
            'has_more': has_more,
            'next_page': page + 1
        })
    
    # Regular page load
    return render(request, "barlery/calendar.html", {
        "upcoming_events": events_page,
        "has_more": has_more,
        "total_events": all_events.count()
    })

def venue(request):
    if request.method == "POST":
        form = EventRequestForm(request.POST)
        if form.is_valid():
            event_request = form.save()
            
            # Send email notification to staff
            send_venue_request_email(event_request)
            
            messages.success(
                request,
                "Thanks! Your event request has been submitted. We'll be in touch soon."
            )
            return redirect("/success?type=venue")
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

            # Send email
            success = send_contact_email(name, email, subject, message)
            
            if success:
                messages.success(request, "Thanks! We received your message. We'll be in touch soon.")
                return redirect("/success?type=contact")
            else:
                messages.error(
                    request, 
                    "Sorry, there was a problem sending your message. Please try again later or contact us directly."
                )
    else:
        form = ContactForm()

    hours = WeeklyHours.load()
    return render(request, "barlery/contact.html", {"form": form, "hours": hours})

def privacy(request):
    return render(request, "barlery/privacy.html")


def success(request):
    """
    Success page shown after form submissions.
    Accepts 'type' query parameter to customize message (contact, venue, etc.)
    """
    return render(request, "barlery/success.html")

def successful_logout(request):
    return render(request, "barlery/index.html")