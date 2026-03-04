from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('appointment/', views.appointment, name='appointment'),
    path('review/submit/', views.review_submit, name='review_submit'),
    path('dashboard/', views.dashboard_index, name='dashboard_index'),
]
