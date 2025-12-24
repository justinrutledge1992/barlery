from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

User = get_user_model()
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.utils import timezone

from .forms import ContactForm, EventRequestForm, BarleryUserCreationForm
from .models import Event, WeeklyHours, EventRequest
from .mailers import send_contact_email, send_venue_request_email, send_new_user_email, send_user_activation_email

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


@staff_member_required(login_url='/accounts/login/')
def account_management(request):
    pending_users = User.objects.filter(
        is_active=False,
        last_login__isnull=True
    ).order_by('-date_joined')

    active_users = User.objects.filter(is_active=True).order_by('-date_joined')

    deactivated_users = User.objects.filter(
        is_active=False,
        last_login__isnull=False
    ).order_by('-date_joined')

    context = {
        'pending_users': pending_users,
        'users': active_users,
        'deactivated_users': deactivated_users,
    }
    return render(request, 'barlery/account_management.html', context)


def user_create(request):
    """
    Public page for creating new user accounts.
    Creates inactive users that must be activated by staff.
    """
    if request.method == 'POST':
        form = BarleryUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Send notification email to staff
            send_new_user_email(user)
            
            messages.success(
                request,
                f"Account created successfully! A staff member will review and activate your account soon."
            )
            return redirect('/success?type=user_created')
    else:
        form = BarleryUserCreationForm()
    
    return render(request, 'barlery/user_create.html', {'form': form})


@staff_member_required(login_url='/accounts/login/')
@require_POST
def deactivate_user(request, user_id):
    """
    Staff-only endpoint to deactivate a user account.
    Sets is_active to False for the specified user.
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Prevent deactivating superusers
        if user.is_superuser:
            return JsonResponse({
                'success': False,
                'error': 'Cannot deactivate superuser accounts'
            }, status=403)
        
        # Prevent staff from deactivating themselves
        if user.id == request.user.id:
            return JsonResponse({
                'success': False,
                'error': 'You cannot deactivate your own account'
            }, status=403)
        
        # Deactivate the user
        user.is_active = False
        user.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Account for {user.first_name} {user.last_name} has been deactivated'
        })
        
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'User not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@staff_member_required(login_url='/accounts/login/')
@require_POST
def activate_user(request, user_id):
    """
    Staff-only endpoint to activate a pending user account.
    Sets is_active to True for the specified user.
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Check if user is already active
        if user.is_active:
            return JsonResponse({
                'success': False,
                'error': 'User is already active'
            }, status=400)
        
        # Activate the user
        user.is_active = True
        user.save()
        
        # Send notification email to staff
        send_user_activation_email(user)
        
        return JsonResponse({
            'success': True,
            'message': f'Account for {user.first_name} {user.last_name} has been activated'
        })
        
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'User not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def custom_login(request):
    """
    Custom login view with success message.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.email}!")
            
            # Redirect to 'next' parameter or home
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('barlery:index')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def custom_logout(request):
    """
    Custom logout view with success message.
    Logs out the user and displays the login page with a success message.
    """
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, "You have been successfully logged out.")
        # Render login template instead of redirecting
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    
    # If GET request, redirect to home
    return redirect('barlery:index')