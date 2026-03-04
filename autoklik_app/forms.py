from django import forms
from .models import Appointment, ContactMessage, Service, Review

class AppointmentForm(forms.ModelForm):
    requested_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full bg-transparent border-b border-iron-800 focus:border-forge-600 outline-none py-3 text-iron-200 font-display tracking-[0.15em] transition-all'}),
        label="Date et Heure Souhaitée"
    )
    
    class Meta:
        model = Appointment
        fields = [
            'client_name', 'client_phone', 'client_email', 
            'vehicle_brand', 'vehicle_model', 'service', 
            'requested_date', 'description'
        ]
        widgets = {
            'client_name': forms.TextInput(attrs={'placeholder': 'NOM COMPLET', 'class': 'w-full bg-transparent border-b border-iron-800 focus:border-forge-600 outline-none py-3 text-iron-200 font-display tracking-[0.15em] transition-all'}),
            'client_phone': forms.TextInput(attrs={'placeholder': '+237 ...', 'class': 'w-full bg-transparent border-b border-iron-800 focus:border-forge-600 outline-none py-3 text-iron-200 font-display tracking-[0.15em] transition-all'}),
            'client_email': forms.EmailInput(attrs={'placeholder': 'EMAIL (OPTIONNEL)', 'class': 'w-full bg-transparent border-b border-iron-800 focus:border-forge-600 outline-none py-3 text-iron-200 font-display tracking-[0.15em] transition-all'}),
            'vehicle_brand': forms.TextInput(attrs={'placeholder': 'MARQUE (EX: TOYOTA)', 'class': 'w-full bg-transparent border-b border-iron-800 focus:border-forge-600 outline-none py-3 text-iron-200 font-display tracking-[0.15em] transition-all'}),
            'vehicle_model': forms.TextInput(attrs={'placeholder': 'MODÈLE (EX: HILUX)', 'class': 'w-full bg-transparent border-b border-iron-800 focus:border-forge-600 outline-none py-3 text-iron-200 font-display tracking-[0.15em] transition-all'}),
            'service': forms.Select(attrs={'class': 'w-full bg-iron-900 border border-iron-800 focus:border-forge-600 outline-none p-3 text-iron-200 font-display tracking-widest transition-all'}),
            'description': forms.Textarea(attrs={'placeholder': 'DÉCRIVEZ LE PROBLÈME OU L\'ENTRETIEN...', 'rows': 4, 'class': 'w-full bg-transparent border border-iron-800 focus:border-forge-600 outline-none p-4 text-iron-300 font-body transition-all'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'NOM COMPLET', 'class': 'w-full bg-transparent border-b border-iron-800 focus:border-forge-600 outline-none py-3 text-iron-200 font-display tracking-[0.15em] transition-all'}),
            'email': forms.EmailInput(attrs={'placeholder': 'EMAIL@ADRESSE.COM', 'class': 'w-full bg-transparent border-b border-iron-800 focus:border-forge-600 outline-none py-3 text-iron-200 font-display tracking-[0.15em] transition-all'}),
            'message': forms.Textarea(attrs={'placeholder': 'DÉCRIVEZ VOTRE BESOIN...', 'rows': 4, 'class': 'w-full bg-transparent border border-iron-800 focus:border-forge-600 outline-none p-4 text-iron-300 font-body transition-all'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author_name', 'rating', 'comment']
        widgets = {
            'author_name': forms.TextInput(attrs={'placeholder': 'VOTRE NOM', 'class': 'w-full bg-transparent border-b border-iron-800 focus:border-forge-600 outline-none py-3 text-iron-200 font-display tracking-[0.15em] transition-all'}),
            'rating': forms.Select(choices=[(i, f'{i} Étoile{"s" if i > 1 else ""}') for i in range(5, 0, -1)], attrs={'class': 'w-full bg-iron-900 border border-iron-800 focus:border-forge-600 outline-none p-3 text-iron-200 font-display tracking-widest transition-all'}),
            'comment': forms.Textarea(attrs={'placeholder': 'VOTRE EXPÉRIENCE CHEZ AUTOKLIK...', 'rows': 4, 'class': 'w-full bg-transparent border border-iron-800 focus:border-forge-600 outline-none p-4 text-iron-300 font-body transition-all'}),
        }
