from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

from .forms import ContactForm, EventRequestForm

def index(request):
    return render(request, "barlery/index.html")

def about(request):
    return render(request, "barlery/about.html")

def menu(request):
    return render(request, "barlery/menu.html")

def calendar(request):
    return render(request, "barlery/calendar.html")

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
            full_message = f"From: {name} <{email}>\n\n{message}"

            send_mail(
                subject=full_subject,
                message=full_message,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Thanks! We received your message. We’ll be in touch soon.")
            return redirect("barlery:contact")
    else:
        form = ContactForm()

    return render(request, "barlery/contact.html", {"form": form})

def successful_logout(request):
    return render(request, "barlery/index.html")