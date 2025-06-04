from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Dog, Testimonial, AdoptionInquiry, VolunteerApplication, ContactMessage
from .forms import AdoptionInquiryForm, VolunteerApplicationForm, ContactForm


def home(request):
    """Home page view"""
    # Get featured dogs for adoption
    featured_dogs = Dog.objects.filter(status='available', is_featured=True)[:3]
    # Get all available dogs if no featured ones
    if not featured_dogs:
        featured_dogs = Dog.objects.filter(status='available')[:6]
    
    # Get active testimonials
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    # Get total statistics
    total_dogs_rescued = Dog.objects.count()
    total_adoptions = Dog.objects.filter(status='adopted').count()
    available_dogs = Dog.objects.filter(status='available').count()
    
    context = {
        'featured_dogs': featured_dogs,
        'testimonials': testimonials,
        'total_dogs_rescued': total_dogs_rescued,
        'total_adoptions': total_adoptions,
        'available_dogs': available_dogs,
        'adoption_form': AdoptionInquiryForm(),
        'volunteer_form': VolunteerApplicationForm(),
        'contact_form': ContactForm(),

    }
    
    return render(request, 'index.html', context)


def dog_detail(request, dog_id):
    """Dog detail view for adoption"""
    dog = get_object_or_404(Dog, id=dog_id, status='available')
    
    if request.method == 'POST':
        form = AdoptionInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.dog = dog
            inquiry.save()
            
            # Send notification email
            try:
                send_mail(
                    f'Nova solicitação de adoção - {dog.name}',
                    f'Nova solicitação de adoção recebida para {dog.name} de {inquiry.name}.\n'
                    f'Email: {inquiry.email}\nTelefone: {inquiry.phone}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            
            messages.success(request, 'Sua solicitação de adoção foi enviada com sucesso! Entraremos em contato em breve.')
            return redirect('home')
    else:
        form = AdoptionInquiryForm()
    
    context = {
        'dog': dog,
        'form': form,
    }
    
    return render(request, 'dog_detail.html', context)


@require_http_methods(["POST"])
def volunteer_application(request):
    """Handle volunteer application form"""
    form = VolunteerApplicationForm(request.POST)
    
    if form.is_valid():
        application = form.save()
        
        # Send notification email
        try:
            send_mail(
                'Nova inscrição de voluntário',
                f'Nova inscrição de voluntário recebida de {application.name}.\n'
                f'Email: {application.email}\nTelefone: {application.phone}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass
        
        messages.success(request, 'Sua inscrição para voluntário foi enviada com sucesso! Entraremos em contato em breve.')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'Erro no campo {field}: {error}')
    
    return redirect('home')


@require_http_methods(["POST"])
def contact_message(request):
    """Handle contact form"""
    form = ContactForm(request.POST)
    
    if form.is_valid():
        message = form.save()
        
        # Send notification email
        try:
            send_mail(
                f'Nova mensagem de contato - {message.subject}',
                f'Nova mensagem recebida de {message.name}.\n'
                f'Email: {message.email}\nAssunto: {message.subject}\n\n{message.message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass
        
        messages.success(request, 'Sua mensagem foi enviada com sucesso! Responderemos em breve.')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'Erro no campo {field}: {error}')
    
    return redirect('home')





@require_http_methods(["POST"])
def adoption_inquiry(request):
    """Handle adoption inquiry form via AJAX"""
    try:
        dog_id = request.POST.get('dog_id')
        dog = get_object_or_404(Dog, id=dog_id, status='available')
        
        form = AdoptionInquiryForm(request.POST)
        
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.dog = dog
            inquiry.save()
            
            # Send notification email
            try:
                send_mail(
                    f'Nova solicitação de adoção - {dog.name}',
                    f'Nova solicitação de adoção recebida para {dog.name} de {inquiry.name}.\n'
                    f'Email: {inquiry.email}\nTelefone: {inquiry.phone}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            
            return JsonResponse({
                'success': True, 
                'message': 'Sua solicitação de adoção foi enviada com sucesso! Entraremos em contato em breve.'
            })
        else:
            return JsonResponse({
                'success': False, 
                'errors': form.errors
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': 'Ocorreu um erro ao enviar sua solicitação. Tente novamente.'
        })
