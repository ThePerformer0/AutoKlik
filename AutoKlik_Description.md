# 🔧 AutoKlik – Site Web Professionnel pour Garage Automobile

## Résumé du projet

Site web complet pour un garage automobile fictif basé à Yaoundé. Le projet couvre à la fois le **site vitrine public** visible par les clients, et un **espace d'administration** complet pour que le gérant du garage gère son business au quotidien sans toucher au code.

Ce projet est conçu pour démontrer une maîtrise complète du développement full-stack Django : modélisation de données, logique métier, interface admin personnalisée, envoi d'emails, gestion de fichiers médias, et frontend moderne.

---

## 👥 Les deux types d'utilisateurs

### Le client (côté public)
Un habitant de la ville qui cherche un garage fiable. Il arrive sur le site depuis Google ou le bouche-à-oreille, veut comprendre ce que propose le garage, et idéalement prendre rendez-vous directement en ligne sans appeler.

### Le gérant du garage (côté admin)
Le patron du garage. Il n'est pas développeur. Il a besoin d'un tableau de bord simple pour voir ses rendez-vous du jour, valider ou refuser des demandes, et gérer ce qui s'affiche sur son site.

---

## 🌐 PARTIE 1 – Le site public (ce que voit le client)

### Page d'accueil
- Nom du garage, slogan, photo de couverture
- Résumé des services proposés avec icônes
- Bouton "Prendre rendez-vous" visible immédiatement
- Section "Pourquoi nous choisir" (expérience, équipe, garantie)
- Avis clients récents (les 3 derniers validés)
- Localisation avec adresse et lien Google Maps
- Numéro de téléphone cliquable (important sur mobile)

### Page Services
Liste détaillée de tous les services du garage, chacun avec :
- Nom du service (ex : Vidange, Freinage, Climatisation...)
- Description courte
- Prix indicatif ou fourchette de prix (optionnel)
- Image illustrative
- Bouton "Prendre RDV pour ce service"

Les services sont gérés depuis l'admin Django — le gérant peut en ajouter, modifier ou supprimer sans toucher au code.

### Page Prise de rendez-vous
Formulaire en ligne avec les champs suivants :
- Nom complet du client
- Numéro de téléphone
- Email (optionnel)
- Service souhaité (menu déroulant lié aux services en base)
- Description du problème (champ texte libre)
- Date et heure souhaitées (avec calendrier interactif)
- Marque et modèle du véhicule

À la soumission :
- Le client reçoit un email de confirmation automatique avec le récapitulatif
- Le gérant reçoit une notification email pour le nouveau RDV
- Le RDV apparaît dans l'admin avec le statut "En attente"

### Page Avis clients
- Affichage de tous les avis validés par le gérant
- Formulaire pour laisser un avis (nom, note sur 5 étoiles, commentaire)
- Les nouveaux avis ne s'affichent pas immédiatement — ils passent par une validation admin
- Note moyenne calculée automatiquement et affichée en haut de page

### Page À propos
- Histoire du garage, année de création
- Photo et présentation de l'équipe
- Valeurs et engagements
- Certifications ou agréments éventuels

### Page Contact
- Adresse complète
- Téléphone et email
- Horaires d'ouverture (gérés depuis l'admin)
- Formulaire de contact simple (nom, email, message)
- Les messages arrivent dans l'admin et par email au gérant

---

## 🔐 PARTIE 2 – L'espace admin (ce que voit le gérant)

L'admin est accessible sur `/dashboard/` avec identifiant et mot de passe. Ce n'est pas l'admin Django par défaut — c'est une interface personnalisée, propre et adaptée à un non-développeur.

### Tableau de bord principal
À l'ouverture, le gérant voit immédiatement :
- Les rendez-vous du jour avec statut (En attente / Confirmé / Annulé)
- Le nombre de nouveaux avis en attente de validation
- Le nombre de messages non lus dans la boîte contact
- Un compteur de RDV de la semaine

### Gestion des rendez-vous
Liste complète des rendez-vous avec filtres (date, statut, service).
Pour chaque rendez-vous, le gérant peut :
- Voir tous les détails (client, véhicule, service, date souhaitée)
- Confirmer le RDV → le client reçoit un email de confirmation
- Proposer une autre date → le client reçoit un email avec la nouvelle proposition
- Annuler le RDV → le client reçoit un email d'annulation avec explication
- Marquer comme "Terminé" une fois la prestation effectuée

### Gestion des services
Le gérant peut :
- Ajouter un nouveau service (nom, description, prix, image)
- Modifier un service existant
- Activer ou désactiver un service (sans le supprimer)
- Réorganiser l'ordre d'affichage sur le site

### Gestion des avis clients
- Liste des avis en attente avec possibilité de valider ou rejeter
- Liste des avis publiés avec possibilité de les dépublier
- Impossible de modifier le contenu d'un avis (intégrité)

### Gestion des messages contact
- Liste de tous les messages reçus
- Marquage lu/non lu
- Possibilité de répondre directement par email depuis l'interface

### Gestion du contenu du site
Le gérant peut modifier sans toucher au code :
- Les horaires d'ouverture
- Le numéro de téléphone et l'adresse
- Le slogan et le texte d'accueil
- Les photos de l'équipe

---

## 🛠️ Stack technique

| Couche | Technologie | Pourquoi ce choix |
|---|---|---|
| Backend | Django 5.x | Framework principal |
| Base de données | PostgreSQL | Robuste, gratuit |
| Envoi d'emails | Django + Gmail SMTP | Gratuit, simple à configurer |
| Médias (photos) | django-storages + Cloudinary | Stockage des images gratuitement |
| Frontend | Tailwind CSS + HTMX | Interface moderne sans React |
| Formulaires | django-crispy-forms | Formulaires propres rapidement |
| Déploiement | Railway (free tier) | Hébergement gratuit pour la démo |

---

## 🗄️ Modèles Django – Structure de la base de données

### `Service`
```python
class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_display = models.CharField(max_length=100, blank=True)  # Ex: "À partir de 15 000 FCFA"
    image = models.ImageField(upload_to='services/', blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)  # Pour trier l'affichage

    class Meta:
        ordering = ['order']
```

### `Appointment` (Rendez-vous)
```python
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
```

### `Review` (Avis client)
```python
class Review(models.Model):
    author_name = models.CharField(max_length=200)
    rating = models.IntegerField()                # 1 à 5
    comment = models.TextField()
    is_published = models.BooleanField(default=False)  # Validation manuelle
    created_at = models.DateTimeField(auto_now_add=True)
```

### `ContactMessage` (Messages du formulaire contact)
```python
class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

### `GarageSettings` (Paramètres du site)
```python
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
```

---

## 📧 Les emails automatiques à coder

C'est une des fonctionnalités qui impressionne le plus un client non-technique.

| Déclencheur | Destinataire | Contenu |
|---|---|---|
| Nouveau RDV soumis | Client | "Votre demande de RDV a bien été reçue" |
| Nouveau RDV soumis | Gérant | "Nouveau RDV en attente de confirmation" |
| RDV confirmé | Client | "Votre RDV est confirmé – Date et heure" |
| RDV reporté | Client | "Nouvelle proposition de date" |
| RDV annulé | Client | "Votre RDV a été annulé" |
| Nouveau message contact | Gérant | "Nouveau message de contact" |

Tous les emails sont en HTML (template Django) avec le logo et les couleurs du garage.

---

## 🎨 Ce que le projet doit démontrer dans le portfolio

| Compétence | Où elle apparaît dans le projet |
|---|---|
| Modélisation de données | Les 5 modèles bien structurés avec relations FK |
| Logique métier | Workflow des statuts de RDV, validation des avis |
| Interface admin custom | Dashboard gérant avec vue claire et actions rapides |
| Envoi d'emails | 6 emails automatiques avec templates HTML |
| Gestion de médias | Upload et affichage des photos de services et d'équipe |
| Frontend moderne | Tailwind + HTMX pour un rendu pro sans React |
| Sécurité de base | Authentification admin, protection CSRF, variables d'environnement |
| Déploiement | Site en ligne avec URL partageable au client |

---

## ⚙️ Ordre de développement recommandé

1. Mise en place du projet Django et configuration PostgreSQL
2. Créer les 5 modèles et faire les migrations
3. Configurer l'admin Django de base pour tester les modèles
4. Coder les pages publiques (accueil, services, contact) en statique d'abord
5. Connecter les pages aux données de la base
6. Coder le formulaire de prise de rendez-vous
7. Ajouter les emails automatiques
8. Coder le formulaire d'avis clients
9. Construire l'interface admin personnalisée (dashboard gérant)
10. Soigner le design Tailwind et la version mobile
11. Déployer sur Railway et connecter Cloudinary pour les médias

---

## ⚠️ Pièges à éviter

**Ne pas utiliser l'admin Django par défaut comme interface gérant.** Elle est trop technique pour un non-développeur. Construis une vraie interface sur `/dashboard/`.

**Toujours valider les avis avant publication.** Sans ça, n'importe qui peut poster n'importe quoi sur le site du client.

**Rendre le site mobile-first dès le début.** La majorité des clients d'un garage chercheront sur téléphone. Tailwind facilite ça avec ses classes responsive.

**Ne jamais mettre les credentials Gmail dans le code.** Les stocker dans le fichier `.env`.

**Prévoir le cas où le gérant n'a pas d'email client.** Le champ email est optionnel dans le formulaire RDV — les confirmations ne s'envoient que si l'email est renseigné.

---

*Projet fictif développé à des fins de portfolio – Garage "AutoPro Yaoundé"*