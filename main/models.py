from django.db import models
from django.utils import timezone


class Dog(models.Model):
    """Model for dogs available for adoption"""
    GENDER_CHOICES = [
        ('M', 'Macho'),
        ('F', 'Fêmea'),
    ]
    
    SIZE_CHOICES = [
        ('P', 'Pequeno'),
        ('M', 'Médio'),
        ('G', 'Grande'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Disponível'),
        ('adopted', 'Adotado'),
        ('pending', 'Adoção Pendente'),
    ]
    
    name = models.CharField('Nome', max_length=100)
    age = models.PositiveIntegerField('Idade (anos)', null=True, blank=True)
    age_months = models.PositiveIntegerField('Idade (meses)', null=True, blank=True)
    gender = models.CharField('Sexo', max_length=1, choices=GENDER_CHOICES)
    size = models.CharField('Porte', max_length=1, choices=SIZE_CHOICES)
    breed = models.CharField('Raça', max_length=100, blank=True)
    description = models.TextField('Descrição')
    personality = models.TextField('Personalidade', blank=True)
    special_needs = models.TextField('Necessidades Especiais', blank=True)
    photo_url = models.URLField('URL da Foto', blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='available')
    is_featured = models.BooleanField('Destaque', default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Cão'
        verbose_name_plural = 'Cães'
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def age_display(self):
        """Return formatted age display"""
        if self.age and self.age > 0:
            return f"{self.age} anos"
        elif self.age_months:
            return f"{self.age_months} meses"
        return "Idade não informada"


class Testimonial(models.Model):
    """Model for adoption testimonials"""
    adopter_name = models.CharField('Nome do Adotante', max_length=100)
    dog_name = models.CharField('Nome do Cão', max_length=100)
    testimonial = models.TextField('Depoimento')
    photo_before_url = models.URLField('Foto Antes (URL)', blank=True)
    photo_after_url = models.URLField('Foto Depois (URL)', blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Depoimento'
        verbose_name_plural = 'Depoimentos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.adopter_name} - {self.dog_name}"


class AdoptionInquiry(models.Model):
    """Model for adoption inquiries"""
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, verbose_name='Cão')
    name = models.CharField('Nome Completo', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Telefone', max_length=20)
    address = models.TextField('Endereço')
    has_experience = models.BooleanField('Tem experiência com cães?', default=False)
    living_situation = models.TextField('Situação de moradia')
    motivation = models.TextField('Por que quer adotar?')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    status = models.CharField('Status', max_length=20, choices=[
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ], default='pending')
    
    class Meta:
        verbose_name = 'Solicitação de Adoção'
        verbose_name_plural = 'Solicitações de Adoção'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.dog.name}"


class VolunteerApplication(models.Model):
    """Model for volunteer applications"""
    name = models.CharField('Nome Completo', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Telefone', max_length=20)
    age = models.PositiveIntegerField('Idade')
    availability = models.TextField('Disponibilidade')
    skills = models.TextField('Habilidades/Experiência')
    motivation = models.TextField('Por que quer ser voluntário?')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    status = models.CharField('Status', max_length=20, choices=[
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ], default='pending')
    
    class Meta:
        verbose_name = 'Inscrição Voluntário'
        verbose_name_plural = 'Inscrições Voluntários'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    """Model for general contact messages"""
    name = models.CharField('Nome', max_length=100)
    email = models.EmailField('Email')
    subject = models.CharField('Assunto', max_length=200)
    message = models.TextField('Mensagem')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    is_read = models.BooleanField('Lida', default=False)
    
    class Meta:
        verbose_name = 'Mensagem de Contato'
        verbose_name_plural = 'Mensagens de Contato'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class Newsletter(models.Model):
    """Model for newsletter subscriptions"""
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Inscrito em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Inscrição Newsletter'
        verbose_name_plural = 'Inscrições Newsletter'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
