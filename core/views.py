from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Appointment, Review, ContactMessage, GarageSettings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.db.models import Q
from datetime import timedelta

def index(request):
    """
    Page d'accueil : Affiche les 4 premiers services, les 3 meilleurs avis
    et les informations du garage (À propos).
    """
    services = Service.objects.filter(is_active=True)[:4]
    reviews = Review.objects.filter(is_published=True).order_by('-rating')[:3]
    settings = GarageSettings.objects.first()
    
    context = {
        'services': services,
        'reviews': reviews,
        'settings': settings,
    }
    return render(request, 'core/index.html', context)

def service_list(request):
    """
    Liste complète de tous les services du garage.
    """
    services = Service.objects.filter(is_active=True)
    return render(request, 'core/services.html', {'services': services})

def appointment_request(request):
    """
    Gestion du formulaire de prise de rendez-vous.
    """
    if request.method == 'POST':
        # Extraction des données du formulaire
        client_name = request.POST.get('name')
        client_phone = request.POST.get('phone')
        client_email = request.POST.get('email')
        service_id = request.POST.get('service')
        vehicle_brand = request.POST.get('brand')
        vehicle_model = request.POST.get('model')
        requested_date = request.POST.get('date')
        description = request.POST.get('message')

        # Création du rendez-vous en base
        service = Service.objects.get(id=service_id) if service_id else None
        
        Appointment.objects.create(
            client_name=client_name,
            client_phone=client_phone,
            client_email=client_email,
            service=service,
            vehicle_brand=vehicle_brand,
            vehicle_model=vehicle_model,
            requested_date=requested_date,
            description=description
        )
        
        messages.success(request, "Votre demande de rendez-vous a bien été envoyée !")
        return redirect('index')

    services = Service.objects.filter(is_active=True)
    return render(request, 'core/appointment.html', {'services': services})

def contact(request):
    """
    Gestion du formulaire de contact simple.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(name=name, email=email, message=message)
        messages.success(request, "Merci pour votre message, nous vous répondrons bientôt.")
        return redirect('index')
        
    return render(request, 'core/contact.html')
        
def review_submit(request):
    """
    Traite la soumission d'un avis client depuis la modale de l'index.
    """
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if author_name and rating and comment:
            Review.objects.create(
                author_name=author_name,
                rating=rating,
                comment=comment,
                is_published=False  # Toujours en attente de validation
            )
            messages.success(request, "Merci ! Votre avis a été envoyé et est en attente de validation.")
        else:
            messages.error(request, "Veuillez remplir tous les champs du formulaire.")
            
    return redirect('index')

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD VIEWS (Espace Admin)
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def dashboard_home(request):
    """
    Accueil du dashboard : Statistiques clés et RDV du jour.
    """
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday()) # Lundi
    
    # ── KPIs (Variables accordées avec le HTML de home.html) ──
    today_appointments = Appointment.objects.filter(requested_date__date=today).order_by('requested_date')
    
    context = {
        'today_count': today_appointments.count(),
        'pending_count': Appointment.objects.filter(status='pending').count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'pending_reviews': Review.objects.filter(is_published=False).count(),
        
        'today_appointments': today_appointments,
        
        # Stats semaine
        'week_count': Appointment.objects.filter(requested_date__date__gte=start_of_week).count(),
        'week_confirmed': Appointment.objects.filter(requested_date__date__gte=start_of_week, status='confirmed').count(),
        'week_pending': Appointment.objects.filter(requested_date__date__gte=start_of_week, status='pending').count(),
        'week_done': Appointment.objects.filter(requested_date__date__gte=start_of_week, status='done').count(),
        
        # Listes latérales
        'recent_reviews': Review.objects.all().order_by('-created_at')[:3],
        'recent_messages': ContactMessage.objects.all().order_by('-created_at')[:3],
    }
    return render(request, 'core/dashboard/home.html', context)

@login_required
def appointment_manage(request):
    """
    Gestion complète des rendez-vous avec filtres et recherche.
    """
    status_filter = request.GET.get('status')
    query = request.GET.get('q')
    
    appointments = Appointment.objects.all().order_by('-requested_date')
    
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    if query:
        appointments = appointments.filter(
            Q(client_name__icontains=query) | 
            Q(vehicle_brand__icontains=query) | 
            Q(vehicle_model__icontains=query)
        )
        
    return render(request, 'core/dashboard/appointments.html', {'appointments': appointments})

@login_required
def appointment_detail(request, pk):
    """
    Affiche le détail complet d'un rendez-vous.
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'core/dashboard/appointment_detail.html', {'appt': appointment})

@login_required
def update_appointment_status(request, pk):
    """
    Met à jour le statut d'un rendez-vous. HTMX Friendly.
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            messages.success(request, f"Statut mis à jour.")
            
            if request.headers.get('HX-Request'):
                # Retourne juste le badge pour HTMX
                badge_class = f"appt-badge appt-badge-{new_status}"
                return HttpResponse(f'<span id="badge-{appointment.pk}" class="{badge_class}">{appointment.get_status_display()}</span>')
                
    return redirect('appointment_manage')

@login_required
def review_list(request):
    """
    Gestion des avis clients avec filtre de publication.
    """
    filter_type = request.GET.get('filter')
    reviews = Review.objects.all().order_by('-created_at')
    
    if filter_type == 'pending':
        reviews = reviews.filter(is_published=False)
    elif filter_type == 'published':
        reviews = reviews.filter(is_published=True)
        
    return render(request, 'core/dashboard/reviews.html', {'reviews': reviews})

@login_required
def review_toggle(request, pk):
    """
    Valide, rejette ou dépublie un avis.
    """
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'publish':
            review.is_published = True
            review.save()
            messages.success(request, f"Avis de {review.author_name} publié.")
        elif action == 'unpublish':
            review.is_published = False
            review.save()
            messages.info(request, "Avis dépublié.")
        elif action == 'reject':
            review.delete()
            messages.warning(request, "Avis supprimé.")
            
    return redirect('review_list')

@login_required
def message_manage(request):
    """
    Gestion des messages de contact.
    """
    filter_type = request.GET.get('filter')
    contact_messages = ContactMessage.objects.all().order_by('-created_at')
    
    if filter_type == 'unread':
        contact_messages = contact_messages.filter(is_read=False)
    elif filter_type == 'read':
        contact_messages = contact_messages.filter(is_read=True)
        
    return render(request, 'core/dashboard/messages.html', {'messages': contact_messages})

@login_required
def message_toggle_read(request, pk):
    """
    Marque un message comme lu ou non lu.
    """
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.is_read = not msg.is_read
        msg.save()
    return redirect('message_manage')

@login_required
def message_delete(request, pk):
    """
    Supprime un message de contact.
    """
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.warning(request, "Message supprimé.")
    return redirect('message_manage')

@login_required
def service_manage(request):
    """
    Gestion du catalogue des services.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        
        Service.objects.create(
            name=name, 
            description=description, 
            price=price if price else None
        )
        messages.success(request, f"Service '{name}' ajouté au catalogue.")
        return redirect('service_manage')

    services = Service.objects.all().order_by('name')
    return render(request, 'core/dashboard/services.html', {'services': services})

@login_required
def service_toggle(request, pk):
    """
    Active ou désactive un service (is_active).
    """
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.is_active = not service.is_active
        service.save()
        status = "activé" if service.is_active else "désactivé"
        messages.info(request, f"Service '{service.name}' {status}.")
    return redirect('service_manage')

@login_required
def garage_settings(request):
    """
    Modification des informations globales du garage (adresse, téléphone, etc.).
    """
    settings = GarageSettings.objects.first()
    
    if request.method == 'POST':
        if not settings:
            settings = GarageSettings()
            
        settings.garage_name = request.POST.get('name')
        settings.address = request.POST.get('address')
        settings.phone = request.POST.get('phone')
        settings.email = request.POST.get('email')
        settings.slogan = request.POST.get('description')
        settings.opening_hours = request.POST.get('opening_hours')
        settings.save()
        
        messages.success(request, "Paramètres du garage mis à jour avec succès.")
        return redirect('garage_settings')

    return render(request, 'core/dashboard/settings.html', {'settings': settings})

def logout_view(request):
    """
    Déconnexion sécurisée de l'utilisateur.
    """
    django_logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('index')
