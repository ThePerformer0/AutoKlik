from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Service, Appointment, Review, ContactMessage, GarageSettings
from .forms import AppointmentForm, ContactForm, ReviewForm

def home(request):
    services = Service.objects.filter(is_active=True)[:3]
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')[:3]
    settings_obj = GarageSettings.objects.first()
    return render(request, 'home.html', {
        'services': services,
        'reviews': reviews,
        'settings': settings_obj
    })

def services(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services_list.html', {'services': services})

def about(request):
    settings_obj = GarageSettings.objects.first()
    return render(request, 'about.html', {'settings': settings_obj})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message_obj = form.save()
            
            # Email Notification (Manager)
            try:
                send_mail(
                    f"Nouveau Message de {message_obj.name}",
                    f"Email: {message_obj.email}\n\nMessage:\n{message_obj.message}",
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except:
                pass

            messages.success(request, "VOTRE MESSAGE A ÉTÉ TRANSMIS AVEC SUCCÈS À NOTRE ÉQUIPE.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save()
            
            # Email Notification (Manager)
            try:
                send_mail(
                    f"Nouveau Rendez-vous: {appt.client_name}",
                    f"Client: {appt.client_name}\nTél: {appt.client_phone}\nVéhicule: {appt.vehicle_brand} {appt.vehicle_model}\nService: {appt.service.name}\nDate souhaitée: {appt.requested_date}",
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except:
                pass

            messages.success(request, "VOTRE DEMANDE DE RENDEZ-VOUS A ÉTÉ ENREGISTRÉE. UNE CONFIRMATION VOUS SERA ENVOYÉE.")
            return redirect('home')
    else:
        # Pré-remplir le service si passé en paramètre d'URL
        service_id = request.GET.get('service')
        initial_data = {}
        if service_id:
            initial_data['service'] = service_id
        form = AppointmentForm(initial=initial_data)
    
    return render(request, 'appointment_form.html', {'form': form})

def review_submit(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('HX-Request'):
                return render(request, 'partials/review_success.html')
            messages.success(request, "MERCI ! VOTRE AVIS A ÉTÉ ENVOYÉ POUR MODÉRATION.")
            return redirect('home')
    else:
        form = ReviewForm()
    
    template = 'review_form.html'
    if request.headers.get('HX-Request'):
        template = 'partials/review_form_partial.html'
        
    return render(request, template, {'form': form})

@login_required
def dashboard_index(request):
    # Stats
    today = timezone.now().date()
    appt_today = Appointment.objects.filter(requested_date__date=today).count()
    pending_appt = Appointment.objects.filter(status='PENDING').count()
    pending_reviews = Review.objects.filter(is_published=False).count()
    total_services = Service.objects.count()
    
    # Recent Data
    recent_appts = Appointment.objects.all().order_by('-requested_date')[:10]
    recent_messages = ContactMessage.objects.all().order_by('-created_at')[:5]
    
    return render(request, 'dashboard/index.html', {
        'appt_today': appt_today,
        'pending_appt': pending_appt,
        'pending_reviews': pending_reviews,
        'total_services': total_services,
        'recent_appts': recent_appts,
        'recent_messages': recent_messages
    })
