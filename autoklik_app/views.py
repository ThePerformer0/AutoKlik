from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def home(request):
    services = Service.objects.filter(is_active=True)[:3]
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')[:3]
    settings = GarageSettings.objects.first()
    return render(request, 'home.html', {
        'services': services,
        'reviews': reviews,
        'settings': settings
    })

def services(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services_list.html', {'services': services})

def about(request):
    settings = GarageSettings.objects.first()
    return render(request, 'about.html', {'settings': settings})

def contact(request):
    if request.method == 'POST':
        # Logique de traitement simplifiée pour le moment
        messages.success(request, "Merci ! Votre message a bien été envoyé.")
        return redirect('contact')
    return render(request, 'contact.html')

def appointment(request):
    services = Service.objects.filter(is_active=True)
    if request.method == 'POST':
        # Logique simplifiée
        messages.success(request, "Votre demande de rendez-vous a été enregistrée. Nous vous contacterons bientôt.")
        return redirect('home')
    return render(request, 'appointment_form.html', {'services': services})

def dashboard_index(request):
    # Provisoire
    return render(request, 'dashboard/index.html')
