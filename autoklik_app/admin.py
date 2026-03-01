from django.contrib import admin
from .models import Service, Appointment, Review, ContactMessage, GarageSettings

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_display', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'service', 'requested_date', 'status')
    list_filter = ('status', 'service', 'requested_date')
    search_fields = ('client_name', 'client_phone', 'vehicle_model')
    date_hierarchy = 'requested_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating')
    list_editable = ('is_published',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('name', 'email', 'message', 'created_at')

@admin.register(GarageSettings)
class GarageSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Empêche d'ajouter plus d'un objet de réglages
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
