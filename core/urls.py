from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("services/", views.service_list, name="service_list"),
    path("appointment/", views.appointment_request, name="appointment_request"),
    path("contact/", views.contact, name="contact"),
    path("review/submit/", views.review_submit, name="review_submit"),
    
    # Dashboard (Espace Admin)
    path("dashboard/", views.dashboard_home, name="dashboard_home"),
    path("dashboard/appointments/", views.appointment_manage, name="appointment_manage"),
    path("dashboard/appointments/<int:pk>/", views.appointment_detail, name="appointment_detail"),
    path("dashboard/appointments/<int:pk>/status/", views.update_appointment_status, name="update_appointment_status"),
    
    path("dashboard/reviews/", views.review_list, name="review_list"),
    path("dashboard/reviews/<int:pk>/toggle/", views.review_toggle, name="review_toggle"),
    
    path("dashboard/messages/", views.message_manage, name="message_manage"),
    path("dashboard/messages/<int:pk>/toggle-read/", views.message_toggle_read, name="message_toggle_read"),
    path("dashboard/messages/<int:pk>/delete/", views.message_delete, name="message_delete"),
    
    path("dashboard/services/", views.service_manage, name="service_manage"),
    path("dashboard/services/<int:pk>/toggle/", views.service_toggle, name="service_toggle"),
    path("dashboard/settings/", views.garage_settings, name="garage_settings"),
    
    path("dashboard/logout/", views.logout_view, name="logout"),
]