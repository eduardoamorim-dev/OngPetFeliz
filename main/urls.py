from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dog/<int:dog_id>/', views.dog_detail, name='dog_detail'),
    path('volunteer/', views.volunteer_application, name='volunteer_application'),
    path('contact/', views.contact_message, name='contact_message'),

    path('adoption/', views.adoption_inquiry, name='adoption_inquiry'),
]
