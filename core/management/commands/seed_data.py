import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Service, Appointment, Review, ContactMessage, GarageSettings

class Command(BaseCommand):
    help = 'Peuple la base de données avec des données fictives pour le test'

    def handle(self, *args, **kwargs):
        self.stdout.write("Purge des données existantes...")
        Service.objects.all().delete()
        Appointment.objects.all().delete()
        Review.objects.all().delete()
        ContactMessage.objects.all().delete()
        GarageSettings.objects.all().delete()

        # 1. Paramètres du Garage
        self.stdout.write("Création des paramètres du garage...")
        settings = GarageSettings.objects.create(
            garage_name="AutoKlik Yaoundé",
            slogan="Votre expert mécanique de confiance",
            phone="+237 670 00 00 00",
            email="contact@autoklik.cm",
            address="Quartier Bastos, Avenue Kennedy, Yaoundé",
            opening_hours="Lun - Sam : 7h - 18h\nDimanche : Fermé",
            google_maps_url="https://goo.gl/maps/example"
        )

        # 2. Services
        self.stdout.write("Création des services...")
        services_data = [
            ("Vidange Complète", "Changement d'huile, filtre à huile et contrôle des points de sécurité.", "À partir de 15 000 FCFA"),
            ("Système de Freinage", "Remplacement des plaquettes, disques et purge du liquide de frein.", "À partir de 25 000 FCFA"),
            ("Diagnostic Électronique", "Lecture des codes défauts et analyse complète des capteurs.", "10 000 FCFA"),
            ("Climatisation", "Recharge de gaz R134a et détection de fuites.", "20 000 FCFA"),
            ("Pneumatiques", "Vente, montage et équilibrage de pneus toutes marques.", "Sur devis"),
        ]
        
        services = []
        for name, desc, price in services_data:
            services.append(Service.objects.create(name=name, description=desc, price_display=price))

        # 3. Avis
        self.stdout.write("Création des avis...")
        reviews_data = [
            ("Jean-Paul M.", 5, "Excellent service ! Rapide et transparent sur les prix. Je recommande vivement."),
            ("Marie N.", 4, "Bonne équipe, l'accueil est sympathique. Travail soigné sur ma climatisation."),
            ("Alain T.", 5, "Le meilleur mécano de Yaoundé pour le diagnostic électronique. Ils ont trouvé la panne en 10 min."),
            ("Samuel E.", 3, "Un peu d'attente mais le résultat est là. Prix corrects."),
            ("Chantal B.", 5, "Service impeccable, ma voiture tourne comme neuve. Merci AutoKlik !"),
        ]
        for name, rating, comment in reviews_data:
            Review.objects.create(
                author_name=name,
                rating=rating,
                comment=comment,
                is_published=random.choice([True, True, False]) # Plus de publiés que de non publiés
            )

        # 4. Messages
        self.stdout.write("Création des messages...")
        messages_data = [
            ("Lucie", "lucie@email.com", "Bonjour, faites-vous le parallélisme ?"),
            ("Robert", "robert@email.com", "Devis pour une courroie sur Toyota Yaris svp."),
            ("Mireille", "mireille@email.com", "Est-ce que vous travaillez le dimanche exceptionnellement ?"),
            ("Gervais", "gervais@email.com", "Vendez-vous des pièces détachées d'occasion ?"),
        ]
        for name, email, msg in messages_data:
            ContactMessage.objects.create(name=name, email=email, message=msg, is_read=random.choice([True, False]))

        # 5. Rendez-vous
        self.stdout.write("Création des rendez-vous...")
        clients = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace"]
        brands = ["Toyota", "Mercedes", "Hyundai", "Nissan", "Volkswagen"]
        models = ["Corolla", "Classe C", "Tucson", "Sunny", "Golf 7"]
        statuses = ['pending', 'confirmed', 'done', 'cancelled']
        
        now = timezone.now()
        
        for i in range(15):
            client = random.choice(clients)
            brand = random.choice(brands)
            model = random.choice(models)
            service = random.choice(services)
            status = random.choice(statuses)
            
            # Dates réparties (passé, présent, futur)
            offset = random.randint(-5, 5)
            requested_date = now + timedelta(days=offset, hours=random.randint(0, 8))
            
            Appointment.objects.create(
                client_name=f"{client} {random.choice('ABCDE')}",
                client_phone=f"+237 699 {random.randint(100000, 999999)}",
                client_email=f"{client.lower()}@test.com",
                vehicle_brand=brand,
                vehicle_model=model,
                service=service,
                status=status,
                requested_date=requested_date
            )

        self.stdout.write(self.style.SUCCESS("Peuplement terminé avec succès !"))
