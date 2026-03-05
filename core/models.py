from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_display = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='services/', blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)  # Pour trier l'affichage

    class Meta:
        ordering = ['order']


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('rescheduled', 'Reporté'),
        ('cancelled', 'Annulé'),
        ('done', 'Terminé'),
    ]

    # Infos client
    client_name = models.CharField(max_length=200)
    client_phone = models.CharField(max_length=20)
    client_email = models.EmailField(blank=True)

    # Infos véhicule
    vehicle_brand = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)

    # Infos RDV
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    requested_date = models.DateTimeField()       # Date souhaitée par le client
    confirmed_date = models.DateTimeField(null=True, blank=True)  # Date confirmée par le gérant

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_note = models.TextField(blank=True)     # Note interne du gérant
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    author_name = models.CharField(max_length=200)
    rating = models.IntegerField() # 1 à 5
    comment = models.TextField()
    is_published = models.BooleanField(default=False)  # Validation manuelle
    created_at = models.DateTimeField(auto_now_add=True)


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class GarageSettings(models.Model):
    # Un seul enregistrement en base — le gérant le modifie depuis l'admin
    garage_name = models.CharField(max_length=200)
    slogan = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    opening_hours = models.TextField()           # Ex: "Lun-Sam : 7h-18h"
    google_maps_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Paramètres du garage"