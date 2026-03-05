from django.contrib import admin
from .models import *

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_display', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'service', 'requested_date', 'status')
    list_filter = ('status', 'service', 'requested_date')
    search_fields = ('client_name', 'client_phone', 'vehicle_brand')
    date_hierarchy = 'requested_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating')
    list_editable = ('is_published',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_read', 'created_at')
    list_filter = ('is_read',)
    list_editable = ('is_read',)

@admin.register(GarageSettings)
class GarageSettingsAdmin(admin.ModelAdmin):
    list_display = ('garage_name', 'phone', 'email')
