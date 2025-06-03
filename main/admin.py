from django.contrib import admin
from django.utils.html import format_html
from .models import Dog, Testimonial, AdoptionInquiry, VolunteerApplication, ContactMessage, Newsletter


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['name', 'age_display', 'gender', 'size', 'status', 'is_featured', 'created_at']
    list_filter = ['status', 'gender', 'size', 'is_featured', 'created_at']
    search_fields = ['name', 'breed', 'description']
    list_editable = ['status', 'is_featured']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'age', 'age_months', 'gender', 'size', 'breed')
        }),
        ('Descrição', {
            'fields': ('description', 'personality', 'special_needs')
        }),
        ('Status e Visibilidade', {
            'fields': ('status', 'is_featured', 'photo_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def age_display(self, obj):
        return obj.age_display
    age_display.short_description = 'Idade'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['adopter_name', 'dog_name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['adopter_name', 'dog_name', 'testimonial']
    list_editable = ['is_active']
    readonly_fields = ['created_at']


@admin.register(AdoptionInquiry)
class AdoptionInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'dog', 'email', 'phone', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'has_experience']
    search_fields = ['name', 'email', 'dog__name']
    list_editable = ['status']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Informações do Interessado', {
            'fields': ('name', 'email', 'phone', 'address')
        }),
        ('Adoção', {
            'fields': ('dog', 'status')
        }),
        ('Detalhes', {
            'fields': ('has_experience', 'living_situation', 'motivation')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'age', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email']
    list_editable = ['status']
    readonly_fields = ['created_at']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    list_editable = ['is_read']
    readonly_fields = ['created_at']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['email', 'name']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
