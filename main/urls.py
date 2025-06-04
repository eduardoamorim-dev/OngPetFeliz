from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dog/<int:dog_id>/', views.dog_detail, name='dog_detail'),
    path('volunteer/', views.volunteer_application, name='volunteer_application'),
    path('contact/', views.contact_message, name='contact_message'),
    path('adoption/', views.adoption_inquiry, name='adoption_inquiry'),
    
    # Admin Dashboard
    path('gestao/', views.admin_dashboard, name='admin_dashboard'),
    
    # API endpoints
    path('admin/api/dashboard/', views.api_dashboard, name='api_dashboard'),
    path('admin/api/dogs/', views.api_dogs, name='api_dogs'),
    path('admin/api/dogs/<int:dog_id>/toggle-featured/', views.api_toggle_dog_featured, name='api_toggle_dog_featured'),
    path('admin/api/adoptions/', views.api_adoptions, name='api_adoptions'),
    path('admin/api/adoptions/<int:adoption_id>/', views.api_update_adoption, name='api_update_adoption'),
    path('admin/api/volunteers/', views.api_volunteers, name='api_volunteers'),
    path('admin/api/volunteers/<int:volunteer_id>/', views.api_update_volunteer, name='api_update_volunteer'),
    path('admin/api/messages/', views.api_messages, name='api_messages'),
    path('admin/api/testimonials/', views.api_testimonials, name='api_testimonials'),
    path('admin/api/testimonials/<int:testimonial_id>/toggle/', views.api_toggle_testimonial, name='api_toggle_testimonial'),
]
