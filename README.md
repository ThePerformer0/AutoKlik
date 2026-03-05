# 🔧 AutoKlik – Gestion de Garage Automobile & Site Vitrine

[![Déployé sur Render](https://img.shields.io/badge/Render-Déployé-success?style=for-the-badge&logo=render)](https://autoklik.onrender.com)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)

**AutoKlik** est une application web complète pour un garage automobile (Yaoundé, Cameroun). Elle combine un **site vitrine professionnel** pour les clients et un **Dashboard d'administration sur-mesure** pour le gérant.

---

🔗 **Démo Live** : [https://autoklik.onrender.com](https://autoklik.onrender.com)

> [!IMPORTANT]
> **Accès Dashboard (Démo)** :
> - **URL** : `/dashboard/`
> - **Utilisateur** : `admin`
> - **Mot de passe** : `admin123`

---

## 🌟 Fonctionnalités Clés

### 🌐 Site Public (Client)
- **Accueil Dynamique** : Présentation du garage, services phares et top avis clients.
- **Catalogue de Services** : Liste complète des prestations avec tarifs indicatifs.
- **Prise de RDV en ligne** : Formulaire interactif avec sélection de service et date souhaitée.
- **Système d'Avis** : Modale de soumission d'avis avec sélecteur d'étoiles (soumis à validation).
- **Contact & Localisation** : Coordonnées dynamiques et lien Google Maps.

### 📊 Dashboard Admin (Gérant)
- **Tableau de Bord KPI** : Statistiques hebdomadaires, vues sur les rendez-vous du jour et messages non lus.
- **Gestion des RDV** : Système complet de filtrage, recherche et mise à jour des statuts (HTMX).
- **Modération des Avis** : Valider, rejeter ou dépublier les commentaires clients.
- **Gestion du Catalogue** : Ajouter, modifier ou désactiver des services en temps réel.
- **Paramètres du Garage** : Modifier le nom, le slogan, les horaires et les coordonnées sans toucher au code.

---

## 🛠️ Stack Technique

- **Backend** : Python 3.12 & Django 6.0
- **Frontend** : Tailwind CSS (Design premium), HTMX (Interactions sans rechargement)
- **Base de données** : SQLite (Optimisé pour démo/portfolio)
- **DevOps** : Docker (Multi-stage build), WhiteNoise (Fichiers statiques)
- **Hébergement** : Render.com

---

## 🚀 Installation Locale

### Avec Docker (Recommandé)
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/ThePerformer0/AutoKlik.git
   cd AutoKlik
   ```
2. Lancez le conteneur :
   ```bash
   docker build -t autoklik .
   docker run -p 8000:8000 --env SECRET_KEY=votre_cle --env DEBUG=True autoklik
   ```

### Installation Classique
1. Créez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   ```
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Préparez la base :
   ```bash
   python manage.py migrate
   python manage.py seed_data  # Importe les données fictives
   ```
4. Lancez le serveur :
   ```bash
   python manage.py runserver
   ```

---

## 📦 Déploiement sur Render

Le projet est configuré pour un déploiement Docker "Zero Budget" :
1. Créez un **Web Service** sur Render lié à ce dépôt.
2. Ajoutez les variables d'environnement : `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`.
3. Auto-Seeding : Grâce à l'[`entrypoint.sh`](entrypoint.sh), le site est automatiquement peuplé avec des données fictives réalistes à chaque déploiement.

---

*Projet développé à des fins de portfolio – © 2026 AutoKlik Yaoundé*
