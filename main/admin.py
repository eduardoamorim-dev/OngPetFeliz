from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Dog, Testimonial, AdoptionInquiry, VolunteerApplication, ContactMessage


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['photo_thumbnail', 'name', 'age_display', 'gender', 'size', 'status', 'is_featured', 'adoption_count', 'created_at']
    list_filter = ['status', 'gender', 'size', 'is_featured', 'created_at', 'breed']
    search_fields = ['name', 'breed', 'description', 'personality']
    list_editable = ['status', 'is_featured']
    readonly_fields = ['created_at', 'updated_at', 'photo_preview', 'adoption_count']
    actions = ['mark_as_available', 'mark_as_adopted', 'mark_as_featured', 'unmark_as_featured']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'age', 'age_months', 'gender', 'size', 'breed')
        }),
        ('Descrição', {
            'fields': ('description', 'personality', 'special_needs')
        }),
        ('Foto', {
            'fields': ('photo_url', 'photo_preview')
        }),
        ('Status e Visibilidade', {
            'fields': ('status', 'is_featured')
        }),
        ('Informações do Sistema', {
            'fields': ('adoption_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def photo_thumbnail(self, obj):
        if obj.photo_url:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', obj.photo_url)
        return "Sem foto"
    photo_thumbnail.short_description = 'Foto'
    
    def photo_preview(self, obj):
        if obj.photo_url:
            return format_html('<img src="{}" width="200" height="200" style="border-radius: 10px; object-fit: cover;" />', obj.photo_url)
        return "Nenhuma foto disponível"
    photo_preview.short_description = 'Preview da Foto'
    
    def age_display(self, obj):
        return obj.age_display
    age_display.short_description = 'Idade'
    
    def adoption_count(self, obj):
        count = AdoptionInquiry.objects.filter(dog=obj).count()
        if count > 0:
            url = reverse('admin:main_adoptioninquiry_changelist') + f'?dog__id__exact={obj.id}'
            return format_html('<a href="{}">{} solicitações</a>', url, count)
        return "0 solicitações"
    adoption_count.short_description = 'Interesse em Adoção'
    
    # Actions
    def mark_as_available(self, request, queryset):
        updated = queryset.update(status='available')
        self.message_user(request, f'{updated} cães marcados como disponíveis para adoção.')
    mark_as_available.short_description = 'Marcar como disponível para adoção'
    
    def mark_as_adopted(self, request, queryset):
        updated = queryset.update(status='adopted')
        self.message_user(request, f'{updated} cães marcados como adotados.')
    mark_as_adopted.short_description = 'Marcar como adotado'
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} cães marcados como destaque.')
    mark_as_featured.short_description = 'Marcar como destaque'
    
    def unmark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} cães removidos do destaque.')
    unmark_as_featured.short_description = 'Remover do destaque'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['adopter_name', 'dog_name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['adopter_name', 'dog_name', 'testimonial']
    list_editable = ['is_active']
    readonly_fields = ['created_at']


@admin.register(AdoptionInquiry)
class AdoptionInquiryAdmin(admin.ModelAdmin):
    list_display = ['dog_photo', 'name', 'dog', 'email', 'phone', 'status_badge', 'has_experience', 'created_at', 'action_buttons']
    list_filter = ['status', 'created_at', 'has_experience', 'dog__gender', 'dog__size']
    search_fields = ['name', 'email', 'phone', 'dog__name', 'dog__breed']
    readonly_fields = ['created_at', 'dog_info', 'applicant_summary']
    actions = ['approve_adoption', 'reject_adoption', 'mark_as_pending', 'send_follow_up']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Resumo da Solicitação', {
            'fields': ('dog_info', 'applicant_summary', 'status')
        }),
        ('Informações do Interessado', {
            'fields': ('name', 'email', 'phone', 'address')
        }),
        ('Informações sobre a Adoção', {
            'fields': ('dog', 'has_experience', 'living_situation', 'motivation')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def dog_photo(self, obj):
        if obj.dog.photo_url:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />', obj.dog.photo_url)
        return "Sem foto"
    dog_photo.short_description = 'Foto'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'approved': '#10b981', 
            'rejected': '#ef4444'
        }
        labels = {
            'pending': 'Pendente',
            'approved': 'Aprovado',
            'rejected': 'Rejeitado'
        }
        color = colors.get(obj.status, '#6b7280')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, label
        )
    status_badge.short_description = 'Status'
    
    def dog_info(self, obj):
        if obj.dog:
            return format_html(
                '<div style="display: flex; align-items: center; gap: 10px;">'
                '<img src="{}" width="60" height="60" style="border-radius: 8px; object-fit: cover;" />'
                '<div><strong>{}</strong><br/>'
                '{} • {} • Porte {}<br/>'
                'Status: {}</div></div>',
                obj.dog.photo_url or '/static/images/no-photo.png',
                obj.dog.name,
                obj.dog.age_display,
                obj.dog.get_gender_display(),
                obj.dog.get_size_display(),
                obj.dog.get_status_display()
            )
        return "Nenhum cão selecionado"
    dog_info.short_description = 'Informações do Cão'
    
    def applicant_summary(self, obj):
        experience = "✓ Tem experiência" if obj.has_experience else "✗ Sem experiência"
        return format_html(
            '<div><strong>{}  • {}</strong><br/>'
            '{}<br/>'
            '<small>📍 {}</small></div>',
            obj.name,
            obj.email,
            experience,
            obj.address[:100] + "..." if len(obj.address) > 100 else obj.address
        )
    applicant_summary.short_description = 'Resumo do Candidato'
    
    def action_buttons(self, obj):
        if obj.status == 'pending':
            approve_url = f'/admin/main/adoptioninquiry/{obj.pk}/change/?action=approve'
            reject_url = f'/admin/main/adoptioninquiry/{obj.pk}/change/?action=reject'
            return format_html(
                '<a href="{}" style="background: #10b981; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px; margin-right: 4px;">Aprovar</a>'
                '<a href="{}" style="background: #ef4444; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">Rejeitar</a>',
                approve_url, reject_url
            )
        return "-"
    action_buttons.short_description = 'Ações'
    
    # Actions
    def approve_adoption(self, request, queryset):
        updated = queryset.update(status='approved')
        # Atualizar status dos cães para 'pending' quando aprovado
        for inquiry in queryset:
            if inquiry.dog.status == 'available':
                inquiry.dog.status = 'pending'
                inquiry.dog.save()
        self.message_user(request, f'{updated} solicitações aprovadas. Cães marcados como adoção pendente.')
    approve_adoption.short_description = 'Aprovar solicitações selecionadas'
    
    def reject_adoption(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} solicitações rejeitadas.')
    reject_adoption.short_description = 'Rejeitar solicitações selecionadas'
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} solicitações marcadas como pendentes.')
    mark_as_pending.short_description = 'Marcar como pendente'


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'age', 'status_badge', 'availability_summary', 'created_at', 'action_buttons']
    list_filter = ['status', 'created_at', 'age']
    search_fields = ['name', 'email', 'phone', 'skills', 'motivation']
    readonly_fields = ['created_at', 'volunteer_summary']
    actions = ['approve_volunteer', 'reject_volunteer', 'mark_as_pending']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Resumo do Voluntário', {
            'fields': ('volunteer_summary', 'status')
        }),
        ('Informações Pessoais', {
            'fields': ('name', 'email', 'phone', 'age')
        }),
        ('Disponibilidade e Habilidades', {
            'fields': ('availability', 'skills', 'motivation')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'approved': '#10b981', 
            'rejected': '#ef4444'
        }
        labels = {
            'pending': 'Pendente',
            'approved': 'Aprovado',
            'rejected': 'Rejeitado'
        }
        color = colors.get(obj.status, '#6b7280')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, label
        )
    status_badge.short_description = 'Status'
    
    def availability_summary(self, obj):
        return obj.availability[:50] + "..." if len(obj.availability) > 50 else obj.availability
    availability_summary.short_description = 'Disponibilidade'
    
    def volunteer_summary(self, obj):
        return format_html(
            '<div><strong>{} anos • {}</strong><br/>'
            '<strong>Habilidades:</strong> {}<br/>'
            '<strong>Motivação:</strong> {}<br/>'
            '<strong>Disponibilidade:</strong> {}</div>',
            obj.age,
            obj.email,
            obj.skills[:100] + "..." if len(obj.skills) > 100 else obj.skills,
            obj.motivation[:100] + "..." if len(obj.motivation) > 100 else obj.motivation,
            obj.availability[:100] + "..." if len(obj.availability) > 100 else obj.availability
        )
    volunteer_summary.short_description = 'Resumo do Candidato'
    
    def action_buttons(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a href="javascript:void(0)" onclick="if(confirm(\'Aprovar este voluntário?\')) window.location.href=\'?action=approve&id={}\'" '
                'style="background: #10b981; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px; margin-right: 4px;">Aprovar</a>'
                '<a href="javascript:void(0)" onclick="if(confirm(\'Rejeitar este voluntário?\')) window.location.href=\'?action=reject&id={}\'" '
                'style="background: #ef4444; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">Rejeitar</a>',
                obj.pk, obj.pk
            )
        return "-"
    action_buttons.short_description = 'Ações'
    
    # Actions
    def approve_volunteer(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} candidatos aprovados como voluntários.')
    approve_volunteer.short_description = 'Aprovar candidatos selecionados'
    
    def reject_volunteer(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} candidatos rejeitados.')
    reject_volunteer.short_description = 'Rejeitar candidatos selecionados'
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} candidatos marcados como pendentes.')
    mark_as_pending.short_description = 'Marcar como pendente'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'is_read_badge', 'priority_level', 'created_at', 'action_buttons']
    list_filter = ['is_read', 'created_at', 'subject']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'message_preview']
    actions = ['mark_as_read', 'mark_as_unread', 'mark_high_priority']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Mensagem', {
            'fields': ('subject', 'message_preview', 'is_read')
        }),
        ('Remetente', {
            'fields': ('name', 'email')
        }),
        ('Conteúdo Completo', {
            'fields': ('message',)
        }),
        ('Informações do Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">Lida</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #ef4444; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">Não Lida</span>'
            )
    is_read_badge.short_description = 'Status'
    
    def priority_level(self, obj):
        # Determinar prioridade baseada em palavras-chave
        urgent_keywords = ['urgente', 'emergência', 'ajuda', 'socorro', 'problema']
        adoption_keywords = ['adoção', 'adotar', 'interessado']
        
        message_lower = (obj.subject + ' ' + obj.message).lower()
        
        if any(keyword in message_lower for keyword in urgent_keywords):
            return format_html('<span style="color: #ef4444; font-weight: bold;">🔴 Alta</span>')
        elif any(keyword in message_lower for keyword in adoption_keywords):
            return format_html('<span style="color: #f59e0b; font-weight: bold;">🟡 Média</span>')
        else:
            return format_html('<span style="color: #10b981;">🟢 Normal</span>')
    priority_level.short_description = 'Prioridade'
    
    def message_preview(self, obj):
        preview = obj.message[:200] + "..." if len(obj.message) > 200 else obj.message
        return format_html('<div style="max-width: 400px; padding: 10px; background: #f9fafb; border-radius: 8px;">{}</div>', preview)
    message_preview.short_description = 'Preview da Mensagem'
    
    def action_buttons(self, obj):
        read_action = "unread" if obj.is_read else "read"
        read_label = "Marcar Não Lida" if obj.is_read else "Marcar como Lida"
        read_color = "#f59e0b" if obj.is_read else "#10b981"
        
        return format_html(
            '<a href="?action={}&id={}" style="background: {}; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px; margin-right: 4px;">{}</a>'
            '<a href="mailto:{}?subject=Re: {}" style="background: #3b82f6; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">Responder</a>',
            read_action, obj.pk, read_color, read_label,
            obj.email, obj.subject
        )
    action_buttons.short_description = 'Ações'
    
    # Actions
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} mensagens marcadas como lidas.')
    mark_as_read.short_description = 'Marcar como lidas'
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} mensagens marcadas como não lidas.')
    mark_as_unread.short_description = 'Marcar como não lidas'



