from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dogs/', views.dogs_list, name='dogs_list'),
    path('dog/<int:dog_id>/', views.dog_detail, name='dog_detail'),
    path('volunteer/', views.volunteer_application, name='volunteer_application'),
    path('contact/', views.contact_message, name='contact_message'),
    path('adoption/', views.adoption_inquiry, name='adoption_inquiry'),
    
    # Public API for dogs listing
    path('api/dogs/available/', views.api_dogs_available, name='api_dogs_available'),
    
    # Admin Dashboard
    path('gestao/', views.admin_dashboard, name='admin_dashboard'),
    path('gestao/login/', views.admin_login, name='admin_login'),
    path('gestao/logout/', views.admin_logout, name='admin_logout'),
    
    # API endpoints
    path('gestao/api/dashboard/', views.api_dashboard, name='api_dashboard'),
    path('gestao/api/dogs/', views.api_dogs, name='api_dogs'),
    path('gestao/api/dogs/<int:dog_id>/', views.api_dogs, name='api_dogs_detail'),
    path('gestao/api/dogs/<int:dog_id>/toggle-featured/', views.api_toggle_dog_featured, name='api_toggle_dog_featured'),
    path('gestao/api/adoptions/', views.api_adoptions, name='api_adoptions'),
    path('gestao/api/adoptions/<int:adoption_id>/', views.api_update_adoption, name='api_update_adoption'),
    path('gestao/api/volunteers/', views.api_volunteers, name='api_volunteers'),
    path('gestao/api/volunteers/<int:volunteer_id>/', views.api_update_volunteer, name='api_update_volunteer'),
    path('gestao/api/messages/', views.api_messages, name='api_messages'),
    path('gestao/api/testimonials/', views.api_testimonials, name='api_testimonials'),
    path('gestao/api/testimonials/<int:testimonial_id>/toggle/', views.api_toggle_testimonial, name='api_toggle_testimonial'),
]
