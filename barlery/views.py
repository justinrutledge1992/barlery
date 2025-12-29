from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

User = get_user_model()
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.utils import timezone

from .forms import ContactForm, EventRequestForm, BarleryUserCreationForm, WeeklyHoursForm
from .models import Event, MenuItem, WeeklyHours, EventRequest
from .mailers import send_contact_email, send_venue_request_email, send_new_user_email, send_user_activation_email

def index(request):
    # Get upcoming events (ordered by date, then time)
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date', 'start_time')[:3]
    
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
        last_login__isnull=True,
        is_superuser=False,
    ).order_by('-date_joined')

    active_users = User.objects.filter(is_active=True, is_superuser=False).order_by('-date_joined')

    deactivated_users = User.objects.filter(
        is_active=False,
        last_login__isnull=False,
        is_superuser=False,
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
    Sets is_active to True and sets permission level based on request data.
    """
    try:
        import json
        
        user = User.objects.get(id=user_id)
        # Prevent activating superusers (they shouldn't be in pending state anyway)
        if user.is_superuser:
            return JsonResponse({
                'success': False,
                'error': 'Cannot modify superuser accounts'
            }, status=403)

        
        # Check if user is already active
        if user.is_active:
            return JsonResponse({
                'success': False,
                'error': 'User is already active'
            }, status=400)
        
        # Get permission level from request body
        permission_level = 'basic'  # default
        if request.body:
            try:
                data = json.loads(request.body)
                permission_level = data.get('permission_level', 'basic')
                print(f"DEBUG: Received permission_level: {permission_level}")
                print(f"DEBUG: Full request data: {data}")
            except json.JSONDecodeError as e:
                print(f"DEBUG: JSON decode error: {e}")
                pass
        
        # Activate the user
        user.is_active = True
        
        # Set staff status based on permission level
        if permission_level == 'elevated':
            user.is_staff = True
        else:
            user.is_staff = False
        
        user.save()
        
        # Send notification email to staff
        send_user_activation_email(user)
        
        permission_text = 'Elevated' if user.is_staff else 'Basic'
        
        return JsonResponse({
            'success': True,
            'message': f'Account for {user.first_name} {user.last_name} has been activated with {permission_text} permissions'
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
    next_url = request.GET.get("next") or request.POST.get("next") or ""

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")

            # If they were trying to reach account management, only allow staff
            mgmt_path = reverse("barlery:account_management")  # e.g. "/accounts/management/"
            if next_url and next_url.startswith(mgmt_path):
                return redirect(next_url) if user.is_staff else redirect("barlery:index")

            # Otherwise, honor next if present
            if next_url:
                return redirect(next_url)

            # Default landing
            return redirect("barlery:account_management") if user.is_staff else redirect("barlery:index")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form, "next": next_url})

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
def event_details(request, event_id):
    """
    Display detailed information about a specific event.
    """
    from django.shortcuts import get_object_or_404
    
    event = get_object_or_404(Event, id=event_id)
    
    return render(request, 'barlery/event_details.html', {
        'event': event
    })

from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def event_create(request):
    """
    Create a new event. Requires authentication.
    """
    from .forms import EventForm
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, f"Event '{event.title}' created successfully!")
            return redirect('barlery:event_details', event_id=event.id)
    else:
        form = EventForm()
    
    return render(request, 'barlery/event_create.html', {'form': form})

@login_required(login_url='/accounts/login/')
def event_edit(request, event_id):
    """
    Edit an existing event. Requires authentication.
    """
    from django.shortcuts import get_object_or_404
    from .forms import EventForm
    
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f"Event '{event.title}' updated successfully!")
            return redirect('barlery:event_details', event_id=event.id)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'barlery/event_edit.html', {
        'form': form,
        'event': event
    })

@login_required(login_url='/accounts/login/')
def menu_item_create(request):
    """
    Create a new menu item. Requires authentication.
    """
    from .forms import MenuItemForm
    from django.utils import timezone
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.last_updated = timezone.now()
            item.save()
            messages.success(request, f"Menu item '{item.name}' created successfully!")
            return redirect('barlery:menu')
    else:
        form = MenuItemForm()
    
    return render(request, 'barlery/menu_item_create.html', {'form': form})

@login_required(login_url='/accounts/login/')
def menu_item_edit(request, item_id):
    """
    Edit an existing menu item. Requires authentication.
    """
    from django.shortcuts import get_object_or_404
    from .forms import MenuItemForm
    from django.utils import timezone
    
    item = get_object_or_404(MenuItem, id=item_id)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.last_updated = timezone.now()
            item.save()
            messages.success(request, f"Menu item '{item.name}' updated successfully!")
            return redirect('barlery:menu')
    else:
        form = MenuItemForm(instance=item)
    
    return render(request, 'barlery/menu_item_edit.html', {
        'form': form,
        'item': item
    })

@login_required(login_url='/accounts/login/')
def menu_item_delete(request, item_id):
    """
    Delete a menu item. Requires authentication.
    Only accepts POST requests for safety.
    """
    from django.shortcuts import get_object_or_404
    
    if request.method == 'POST':
        item = get_object_or_404(MenuItem, id=item_id)
        item_name = item.name
        item.delete()
        messages.success(request, f"Menu item '{item_name}' deleted successfully!")
        return redirect('barlery:menu')
    
    # If not POST, redirect to menu
    return redirect('barlery:menu')

@login_required(login_url='/accounts/login/')
def event_delete(request, event_id):
    """
    Delete an event. Requires authentication.
    Only accepts POST requests for safety.
    """
    from django.shortcuts import get_object_or_404
    
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event_title = event.title
        event.delete()
        messages.success(request, f"Event '{event_title}' deleted successfully!")
        return redirect('barlery:calendar')
    
    # If not POST, redirect to calendar
    return redirect('barlery:calendar')

@staff_member_required(login_url='/accounts/login/')
def edit_user(request, user_id):
    """
    Staff-only page to edit user phone number and permissions.
    """
    from .forms import UserEditForm
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('barlery:account_management')
    
    # Prevent editing superusers
    if user.is_superuser:
        messages.error(request, 'Cannot modify superuser accounts.')
        return redirect('barlery:account_management')
    
    # Prevent staff from editing themselves
    if user.id == request.user.id:
        messages.error(request, 'You cannot edit your own account.')
        return redirect('barlery:account_management')
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            # Save phone number
            form.save()
            
            # Update staff status based on permission level
            permission_level = form.cleaned_data.get('permission_level')
            if permission_level == 'elevated':
                user.is_staff = True
            else:
                user.is_staff = False
            user.save()
            
            permission_text = 'Elevated' if user.is_staff else 'Basic'
            messages.success(request, f'Account for {user.first_name} {user.last_name} has been updated with {permission_text} permissions.')
            return redirect('barlery:account_management')
    else:
        form = UserEditForm(instance=user)
    
    context = {
        'form': form,
        'edited_user': user,
    }
    return render(request, 'barlery/user_edit.html', context)

@login_required
def hours_edit(request):
    """Edit weekly business hours (authenticated users only)."""
    hours = WeeklyHours.load()  # Get the singleton instance
    
    if request.method == 'POST':
        form = WeeklyHoursForm(request.POST, instance=hours)
        if form.is_valid():
            form.save()
            messages.success(request, 'Business hours updated successfully!')
            return redirect('barlery:hours_edit')
    else:
        form = WeeklyHoursForm(instance=hours)
    
    return render(request, 'barlery/hours_edit.html', {
        'form': form,
        'hours': hours
    })