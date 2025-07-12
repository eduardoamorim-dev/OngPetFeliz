from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import json

from .models import Dog, Testimonial, AdoptionInquiry, VolunteerApplication, ContactMessage
from .forms import AdoptionInquiryForm, VolunteerApplicationForm, ContactForm


def is_admin_user(user):
    """Check if user is staff/admin"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


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


def dogs_list(request):
    """Dogs listing page view - shows only featured dogs available for adoption"""
    # Get total count of featured dogs available for adoption
    total_dogs = Dog.objects.filter(status='available', is_featured=True).count()
    
    context = {
        'total_dogs': total_dogs,
    }
    
    return render(request, 'dogs_list.html', context)


@require_http_methods(["GET"])
def api_dogs_available(request):
    """API endpoint for available featured dogs"""
    # Only show featured dogs that are available for adoption
    dogs = Dog.objects.filter(
        status='available', 
        is_featured=True
    ).order_by('-created_at')
    
    data = []
    for dog in dogs:
        data.append({
            'id': dog.id,
            'name': dog.name,
            'age': dog.age,
            'age_months': dog.age_months,
            'gender': dog.gender,
            'size': dog.size,
            'breed': dog.breed or '',
            'photo_url': dog.photo_url or '',
            'description': dog.description or '',
            'personality': dog.personality or '',
            'special_needs': dog.special_needs or '',
            'is_featured': dog.is_featured,
            'created_at': dog.created_at.isoformat()
        })
    
    return JsonResponse(data, safe=False)


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
            
            # Return JSON response for AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': 'Sua solicitação de adoção foi enviada com sucesso! Entraremos em contato em breve.'
                })
            else:
                # Redirect for regular form submission
                messages.success(request, 'Sua solicitação de adoção foi enviada com sucesso! Entraremos em contato em breve.')
                return redirect('home')
        else:
            # Return JSON errors for AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'errors': form.errors
                })
            else:
                # Show form errors for regular submission
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'Erro no campo {field}: {error}')
                return redirect('home')
    
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False, 
                'message': 'Ocorreu um erro ao enviar sua solicitação. Tente novamente.'
            })
        else:
            messages.error(request, 'Ocorreu um erro ao enviar sua solicitação. Tente novamente.')
            return redirect('home')


# Authentication Views
def admin_login(request):
    """Admin login view"""
    if request.user.is_authenticated and is_admin_user(request.user):
        return redirect('admin_dashboard')
    
    error_message = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None and is_admin_user(user):
                login(request, user)
                
                # Set session expiry based on remember me
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                else:
                    request.session.set_expiry(1209600)  # 2 weeks
                
                next_url = request.GET.get('next', 'admin_dashboard')
                return redirect(next_url)
            else:
                error_message = "Usuário ou senha inválidos, ou você não tem permissão de administrador."
        else:
            error_message = "Por favor, preencha todos os campos."
    
    context = {
        'error_message': error_message,
        'debug': settings.DEBUG
    }
    return render(request, 'admin_login.html', context)


def admin_logout(request):
    """Admin logout view"""
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('admin_login')


# Admin Dashboard Views
@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    # Get dashboard stats
    dogs_count = Dog.objects.count()
    pending_adoptions = AdoptionInquiry.objects.filter(status='pending').count()
    active_volunteers = VolunteerApplication.objects.filter(status='approved').count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    
    context = {
        'dogs_count': dogs_count,
        'pending_adoptions': pending_adoptions,
        'active_volunteers': active_volunteers,
        'unread_messages': unread_messages,
    }
    
    return render(request, 'admin_dashboard.html', context)


# API Views for Admin Dashboard
@require_http_methods(["GET"])
@login_required
def api_dashboard(request):
    """Dashboard statistics API"""
    from django.db.models import Count
    
    # Basic stats
    stats = {
        'total_dogs': Dog.objects.count(),
        'pending_adoptions': AdoptionInquiry.objects.filter(status='pending').count(),
        'active_volunteers': VolunteerApplication.objects.filter(status='approved').count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
    }
    
    # Recent adoptions
    recent_adoptions = AdoptionInquiry.objects.select_related('dog').filter(
        status__in=['pending', 'approved']
    ).order_by('-created_at')[:5]
    
    stats['recent_adoptions'] = [{
        'id': adoption.id,
        'dog_name': adoption.dog.name,
        'dog_photo': adoption.dog.photo_url or '/static/images/no-photo.png',
        'adopter_name': adoption.name,
        'status': adoption.status,
        'created_at': adoption.created_at.isoformat()
    } for adoption in recent_adoptions]
    
    # Urgent messages
    urgent_keywords = ['urgente', 'emergência', 'ajuda', 'socorro', 'problema']
    urgent_messages = ContactMessage.objects.filter(
        is_read=False
    ).order_by('-created_at')
    
    urgent_list = []
    for message in urgent_messages:
        message_text = (message.subject + ' ' + message.message).lower()
        if any(keyword in message_text for keyword in urgent_keywords):
            urgent_list.append({
                'id': message.id,
                'name': message.name,
                'email': message.email,
                'subject': message.subject,
                'created_at': message.created_at.isoformat()
            })
    
    stats['urgent_messages'] = urgent_list[:5]
    
    return JsonResponse(stats)

@require_http_methods(["GET", "POST", "PUT", "PATCH"])
@csrf_exempt
@login_required
def api_dogs(request, dog_id=None):
    """Dogs API endpoint - Versão com suporte a edição"""
    
    if request.method == 'GET':
        # Código GET existente...
        dogs = Dog.objects.annotate(
            adoption_count=Count('adoptioninquiry')
        ).order_by('-created_at')
        
        data = [{
            'id': dog.id,
            'name': dog.name,
            'age': dog.age,
            'age_months': dog.age_months,
            'gender': dog.gender,
            'size': dog.size,
            'breed': dog.breed or '',
            'photo_url': dog.photo_url or '',
            'description': dog.description or '',
            'personality': dog.personality or '',
            'special_needs': dog.special_needs or '',
            'status': dog.status,
            'is_featured': dog.is_featured,
            'adoption_count': dog.adoption_count,
            'created_at': dog.created_at.isoformat()
        } for dog in dogs]
        
        return JsonResponse(data, safe=False)
    
    elif request.method in ['POST', 'PUT', 'PATCH']:
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # Parse do JSON
            data = json.loads(request.body)
            logger.info(f"Parsed data: {data}")
            
            # Validação de campos obrigatórios (apenas para POST)
            if request.method == 'POST':
                required_fields = ['name', 'gender', 'size']
                for field in required_fields:
                    if not data.get(field) or str(data.get(field)).strip() == '':
                        return JsonResponse({
                            'success': False, 
                            'error': f'Campo {field} é obrigatório'
                        }, status=400)
            
            # Conversão e validação de idade
            try:
                age_raw = data.get('age', 0)
                age = int(float(age_raw)) if age_raw not in [None, '', 'null'] else 0
            except (ValueError, TypeError):
                age = 0
            
            try:
                age_months_raw = data.get('age_months', 0)
                age_months = int(float(age_months_raw)) if age_months_raw not in [None, '', 'null'] else 0
            except (ValueError, TypeError):
                age_months = 0
            
            # Validação de gender
            gender = str(data.get('gender', '')).upper()
            if gender and gender not in ['M', 'F']:
                return JsonResponse({
                    'success': False, 
                    'error': 'Gênero deve ser M ou F'
                }, status=400)
            
            # Validação de size
            size = str(data.get('size', '')).upper()
            if size and size not in ['P', 'M', 'G']:
                return JsonResponse({
                    'success': False, 
                    'error': 'Porte deve ser P (Pequeno), M (Médio) ou G (Grande)'
                }, status=400)
            
            # Conversão de is_featured para boolean
            is_featured_raw = data.get('is_featured', False)
            if isinstance(is_featured_raw, str):
                is_featured = is_featured_raw.lower() in ['true', '1', 'yes', 'on']
            else:
                is_featured = bool(is_featured_raw)
            
            # Sanitização de strings
            def clean_string(value, max_length=None):
                if value is None:
                    return ''
                cleaned = str(value).strip()
                if max_length and len(cleaned) > max_length:
                    cleaned = cleaned[:max_length]
                return cleaned
            
            if request.method == 'POST':
                # Criação do objeto Dog
                dog = Dog.objects.create(
                    name=clean_string(data.get('name'), 100),
                    age=age,
                    age_months=age_months,
                    gender=gender,
                    size=size,
                    breed=clean_string(data.get('breed'), 100),
                    photo_url=clean_string(data.get('photo_url'), 500),
                    description=clean_string(data.get('description'), 1000),
                    personality=clean_string(data.get('personality'), 500),
                    special_needs=clean_string(data.get('special_needs'), 500),
                    is_featured=is_featured
                )
                logger.info(f"Cão criado com sucesso: ID {dog.id}")
                return JsonResponse({'success': True, 'id': dog.id})
            
            else:  # PUT/PATCH
                if not dog_id:
                    return JsonResponse({
                        'success': False, 
                        'error': 'ID do cão é obrigatório para edição'
                    }, status=400)
                
                dog = get_object_or_404(Dog, id=dog_id)
                
                # Atualizar campos
                if data.get('name'):
                    dog.name = clean_string(data.get('name'), 100)
                if 'age' in data:
                    dog.age = age
                if 'age_months' in data:
                    dog.age_months = age_months
                if data.get('gender'):
                    dog.gender = gender
                if data.get('size'):
                    dog.size = size
                if 'breed' in data:
                    dog.breed = clean_string(data.get('breed'), 100)
                if 'photo_url' in data:
                    dog.photo_url = clean_string(data.get('photo_url'), 500)
                if 'description' in data:
                    dog.description = clean_string(data.get('description'), 1000)
                if 'personality' in data:
                    dog.personality = clean_string(data.get('personality'), 500)
                if 'special_needs' in data:
                    dog.special_needs = clean_string(data.get('special_needs'), 500)
                if 'is_featured' in data:
                    dog.is_featured = is_featured
                
                dog.save()
                logger.info(f"Cão atualizado com sucesso: ID {dog.id}")
                return JsonResponse({'success': True, 'id': dog.id})
            
        except Exception as e:
            logger.error(f"Erro inesperado: {e}", exc_info=True)
            return JsonResponse({
                'success': False, 
                'error': f'Erro interno do servidor: {str(e)}'
            }, status=500)


@require_http_methods(["POST"])
@login_required
def api_toggle_dog_featured(request, dog_id):
    """Toggle dog featured status"""
    try:
        dog = get_object_or_404(Dog, id=dog_id)
        dog.is_featured = not dog.is_featured
        dog.save()
        return JsonResponse({'success': True, 'is_featured': dog.is_featured})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
@login_required
def api_adoptions(request):
    """Adoptions API endpoint"""
    adoptions = AdoptionInquiry.objects.select_related('dog').order_by('-created_at')
    
    data = [{
        'id': adoption.id,
        'dog_name': adoption.dog.name,
        'dog_photo': adoption.dog.photo_url or '/static/images/no-photo.png',
        'name': adoption.name,
        'email': adoption.email,
        'phone': adoption.phone,
        'address': adoption.address,
        'has_experience': adoption.has_experience,
        'living_situation': adoption.living_situation,
        'motivation': adoption.motivation,
        'status': adoption.status,
        'created_at': adoption.created_at.isoformat()
    } for adoption in adoptions]
    
    return JsonResponse(data, safe=False)


@require_http_methods(["PATCH"])
@csrf_exempt
@login_required
def api_update_adoption(request, adoption_id):
    """Update adoption status"""
    try:
        data = json.loads(request.body)
        
        # Validação de status
        if data.get('status') not in ['pending', 'approved', 'rejected']:
            return JsonResponse({'success': False, 'error': 'Status inválido'}, status=400)
        
        adoption = get_object_or_404(AdoptionInquiry, id=adoption_id)
        adoption.status = data['status']
        adoption.save()
        
        # Update dog status if adoption is approved
        if data['status'] == 'approved' and adoption.dog.status == 'available':
            adoption.dog.status = 'pending'
            adoption.dog.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
@login_required
def api_volunteers(request):
    """Volunteers API endpoint"""
    volunteers = VolunteerApplication.objects.order_by('-created_at')
    
    data = [{
        'id': volunteer.id,
        'name': volunteer.name,
        'email': volunteer.email,
        'phone': volunteer.phone,
        'age': volunteer.age,
        'availability': volunteer.availability,
        'skills': volunteer.skills,
        'motivation': volunteer.motivation,
        'status': volunteer.status,
        'created_at': volunteer.created_at.isoformat()
    } for volunteer in volunteers]
    
    return JsonResponse(data, safe=False)


@require_http_methods(["PATCH"])
@csrf_exempt
@login_required
def api_update_volunteer(request, volunteer_id):
    """Update volunteer status"""
    try:
        data = json.loads(request.body)
        
        # Validação de status
        if data.get('status') not in ['pending', 'approved', 'rejected']:
            return JsonResponse({'success': False, 'error': 'Status inválido'}, status=400)
        
        volunteer = get_object_or_404(VolunteerApplication, id=volunteer_id)
        volunteer.status = data['status']
        volunteer.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
@login_required
def api_messages(request):
    """Messages API endpoint"""
    messages = ContactMessage.objects.order_by('-created_at')
    
    # Determine priority based on keywords
    urgent_keywords = ['urgente', 'emergência', 'ajuda', 'socorro', 'problema']
    adoption_keywords = ['adoção', 'adotar', 'interessado']
    
    data = []
    for message in messages:
        message_text = (message.subject + ' ' + message.message).lower()
        
        if any(keyword in message_text for keyword in urgent_keywords):
            priority = 'high'
        elif any(keyword in message_text for keyword in adoption_keywords):
            priority = 'medium'
        else:
            priority = 'normal'
        
        data.append({
            'id': message.id,
            'name': message.name,
            'email': message.email,
            'subject': message.subject,
            'message': message.message,
            'is_read': message.is_read,
            'priority': priority,
            'created_at': message.created_at.isoformat()
        })
    
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
@login_required
def api_testimonials(request):
    """Testimonials API endpoint"""
    testimonials = Testimonial.objects.order_by('-created_at')
    
    data = [{
        'id': testimonial.id,
        'adopter_name': testimonial.adopter_name,
        'dog_name': testimonial.dog_name,
        'testimonial': testimonial.testimonial,
        'is_active': testimonial.is_active,
        'created_at': testimonial.created_at.isoformat()
    } for testimonial in testimonials]
    
    return JsonResponse(data, safe=False)


@require_http_methods(["POST"])
@csrf_exempt
@login_required
def api_toggle_testimonial(request, testimonial_id):
    """Toggle testimonial active status"""
    try:
        testimonial = get_object_or_404(Testimonial, id=testimonial_id)
        testimonial.is_active = not testimonial.is_active
        testimonial.save()
        return JsonResponse({'success': True, 'is_active': testimonial.is_active})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
