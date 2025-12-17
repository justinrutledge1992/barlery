from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "barlery/index.html")

def about(request):
    return render(request, "barlery/about.html")

def menu(request):
    return render(request, "barlery/menu.html")

def calendar(request):
    return render(request, "barlery/calendar.html")

def venue(request):
    return render(request, "barlery/venue.html")

def contact(request):
    return render(request, "barlery/contact.html")

def successful_logout(request):
    return render(request, "barlery/index.html")