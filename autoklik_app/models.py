from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_display = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='services/', blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('rescheduled', 'Reporté'),
        ('cancelled', 'Annulé'),
        ('done', 'Terminé'),
    ]

    client_name = models.CharField(max_length=200)
    client_phone = models.CharField(max_length=20)
    client_email = models.EmailField(blank=True)

    vehicle_brand = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)

    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    requested_date = models.DateTimeField()
    confirmed_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"

    def __str__(self):
        return f"{self.client_name} - {self.service} - {self.requested_date.strftime('%d/%m/%Y')}"

class Review(models.Model):
    author_name = models.CharField(max_length=200)
    rating = models.IntegerField()
    comment = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"

    def __str__(self):
        return f"{self.author_name} - {self.rating}/5"

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"Message de {self.name} ({self.created_at.strftime('%d/%m/%Y')})"

class GarageSettings(models.Model):
    garage_name = models.CharField(max_length=200)
    slogan = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    opening_hours = models.TextField()
    google_maps_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Paramètres du garage"
        verbose_name_plural = "Paramètres du garage"

    def __str__(self):
        return self.garage_name
