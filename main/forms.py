from django import forms
from django.core.validators import RegexValidator
from .models import AdoptionInquiry, VolunteerApplication, ContactMessage


class AdoptionInquiryForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\(\d{2}\)\s?\d{4,5}-?\d{4}$',
        message="Telefone deve estar no formato (11) 99999-9999"
    )
    
    phone = forms.CharField(validators=[phone_regex], max_length=15)
    
    class Meta:
        model = AdoptionInquiry
        exclude = ['dog', 'created_at', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Seu nome completo',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'seu@email.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '(11) 99999-9999',
                'required': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Endereço completo',
                'required': True
            }),
            'has_experience': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            }),
            'living_situation': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Descreva sua situação de moradia (casa, apartamento, quintal, etc.)',
                'required': True
            }),
            'motivation': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 4,
                'placeholder': 'Por que você quer adotar este cão?',
                'required': True
            }),
        }
        labels = {
            'name': 'Nome Completo',
            'email': 'Email',
            'phone': 'Telefone',
            'address': 'Endereço',
            'has_experience': 'Tenho experiência com cães',
            'living_situation': 'Situação de Moradia',
            'motivation': 'Por que quer adotar?',
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name.split()) < 2:
            raise forms.ValidationError("Por favor, informe seu nome completo.")
        return name


class VolunteerApplicationForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\(\d{2}\)\s?\d{4,5}-?\d{4}$',
        message="Telefone deve estar no formato (11) 99999-9999"
    )
    
    phone = forms.CharField(validators=[phone_regex], max_length=15)
    
    class Meta:
        model = VolunteerApplication
        exclude = ['created_at', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Seu nome completo',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'seu@email.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': '(11) 99999-9999',
                'required': True
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'min': '18',
                'max': '100',
                'required': True
            }),
            'availability': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Quando você está disponível? (dias da semana, horários)',
                'required': True
            }),
            'skills': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Suas habilidades e experiências relevantes',
                'required': True
            }),
            'motivation': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 4,
                'placeholder': 'Por que você quer ser voluntário?',
                'required': True
            }),
        }
        labels = {
            'name': 'Nome Completo',
            'email': 'Email',
            'phone': 'Telefone',
            'age': 'Idade',
            'availability': 'Disponibilidade',
            'skills': 'Habilidades/Experiência',
            'motivation': 'Motivação',
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name.split()) < 2:
            raise forms.ValidationError("Por favor, informe seu nome completo.")
        return name
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 18 or age > 100):
            raise forms.ValidationError("Idade deve estar entre 18 e 100 anos.")
        return age


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        exclude = ['created_at', 'is_read']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent',
                'placeholder': 'Seu nome',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent',
                'placeholder': 'seu@email.com',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent',
                'placeholder': 'Assunto da mensagem',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent',
                'rows': 5,
                'placeholder': 'Sua mensagem',
                'required': True
            }),
        }
        labels = {
            'name': 'Nome',
            'email': 'Email',
            'subject': 'Assunto',
            'message': 'Mensagem',
        }
    
    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if subject and len(subject) < 5:
            raise forms.ValidationError("Assunto deve ter pelo menos 5 caracteres.")
        return subject
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message) < 10:
            raise forms.ValidationError("Mensagem deve ter pelo menos 10 caracteres.")
        return message



