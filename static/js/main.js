// Main JavaScript for ONG Resgate de Cães

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavigation();
    initModals();
    initForms();
    initScrollEffects();
    initMessageAutoHide();
});

// Navigation functionality
function initNavigation() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Mobile menu toggle
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Smooth scroll for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const offset = 80; // Account for fixed header
                    const targetPosition = target.offsetTop - offset;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                    
                    // Close mobile menu if open
                    if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                        mobileMenu.classList.add('hidden');
                    }
                }
            }
        });
    });

    // Update active navigation link on scroll
    window.addEventListener('scroll', updateActiveNavLink);
}

// Update active navigation link based on scroll position
function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    let current = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.offsetHeight;
        
        if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('text-rescue-blue-600', 'font-semibold');
        link.classList.add('text-gray-700');
        
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.remove('text-gray-700');
            link.classList.add('text-rescue-blue-600', 'font-semibold');
        }
    });
}

// Modal functionality
function initModals() {
    // Close modals when clicking outside
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('fixed') && e.target.classList.contains('inset-0')) {
            closeAllModals();
        }
    });

    // Close modals with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
}

// Open adoption modal
function openAdoptionModal(dogId, dogName) {
    const modal = document.getElementById('adoptionModal');
    const dogIdInput = document.getElementById('dogId');
    const selectedDogName = document.getElementById('selectedDogName');
    
    if (modal && dogIdInput && selectedDogName) {
        dogIdInput.value = dogId;
        selectedDogName.textContent = dogName;
        modal.classList.remove('hidden');
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

// Close adoption modal
function closeAdoptionModal() {
    const modal = document.getElementById('adoptionModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('show');
        document.body.style.overflow = 'auto';
        
        // Reset form
        const form = document.getElementById('adoptionForm');
        if (form) {
            form.reset();
        }
    }
}

// Open volunteer modal
function openVolunteerModal() {
    const modal = document.getElementById('volunteerModal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

// Close volunteer modal
function closeVolunteerModal() {
    const modal = document.getElementById('volunteerModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('show');
        document.body.style.overflow = 'auto';
    }
}

// Close all modals
function closeAllModals() {
    closeAdoptionModal();
    closeVolunteerModal();
}

// Form functionality
function initForms() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('button[type="submit"]');
            
            if (submitButton) {
                // Add loading state
                submitButton.classList.add('loading');
                submitButton.disabled = true;
                
                // Store original text
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Enviando...';
                
                // Reset button after 3 seconds if form doesn't redirect
                setTimeout(() => {
                    if (submitButton) {
                        submitButton.classList.remove('loading');
                        submitButton.disabled = false;
                        submitButton.innerHTML = originalText;
                    }
                }, 3000);
            }
        });
    });

    // Form validation
    addFormValidation();
}

// Add form validation
function addFormValidation() {
    const emailInputs = document.querySelectorAll('input[type="email"]');
    const phoneInputs = document.querySelectorAll('input[name="phone"]');
    
    // Email validation
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateEmail(this);
        });
    });
    
    // Phone validation and formatting
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            formatPhone(this);
        });
    });
}

// Validate email
function validateEmail(input) {
    const email = input.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email && !emailRegex.test(email)) {
        input.classList.add('border-red-500');
        showFieldError(input, 'Por favor, insira um email válido');
    } else {
        input.classList.remove('border-red-500');
        hideFieldError(input);
    }
}

// Format phone number
function formatPhone(input) {
    let value = input.value.replace(/\D/g, '');
    
    if (value.length <= 11) {
        value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
        value = value.replace(/(\d{2})(\d{4})/, '($1) $2');
        value = value.replace(/(\d{2})/, '($1');
    }
    
    input.value = value;
}

// Show field error
function showFieldError(input, message) {
    hideFieldError(input); // Remove existing error
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'text-red-500 text-sm mt-1 field-error';
    errorDiv.textContent = message;
    
    input.parentNode.appendChild(errorDiv);
}

// Hide field error
function hideFieldError(input) {
    const existingError = input.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
}

// Scroll effects
function initScrollEffects() {
    // Fade in elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements that should fade in
    const fadeElements = document.querySelectorAll('.dog-card, .bg-white.rounded-lg.shadow-lg');
    fadeElements.forEach(el => {
        observer.observe(el);
    });

    // Parallax effect for hero section (subtle)
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const hero = document.getElementById('inicio');
        
        if (hero) {
            const rate = scrolled * -0.5;
            hero.style.transform = `translateY(${rate}px)`;
        }
    });
}

// Auto-hide messages
function initMessageAutoHide() {
    const messages = document.querySelectorAll('#messages > div');
    
    messages.forEach(message => {
        setTimeout(() => {
            if (message && message.parentNode) {
                message.style.transition = 'opacity 0.5s ease-out';
                message.style.opacity = '0';
                
                setTimeout(() => {
                    if (message && message.parentNode) {
                        message.remove();
                    }
                }, 500);
            }
        }, 5000); // Hide after 5 seconds
    });
}

// Utility functions
function showLoading(element) {
    if (element) {
        element.classList.add('loading');
        element.disabled = true;
    }
}

function hideLoading(element) {
    if (element) {
        element.classList.remove('loading');
        element.disabled = false;
    }
}

// AJAX form submission for adoption inquiries
function submitAdoptionForm(form) {
    const formData = new FormData(form);
    
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            closeAdoptionModal();
        } else {
            showMessage(data.message || 'Erro ao enviar solicitação', 'error');
        }
    })
    .catch(error => {
        showMessage('Erro ao enviar solicitação. Tente novamente.', 'error');
    });
}

// Show message
function showMessage(message, type = 'info') {
    const messagesContainer = document.getElementById('messages') || createMessagesContainer();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `mb-2 p-4 rounded-lg shadow-lg opacity-0 animate-fade-in ${getMessageClasses(type)}`;
    
    messageDiv.innerHTML = `
        <div class="flex items-center justify-between">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (messageDiv && messageDiv.parentNode) {
            messageDiv.style.opacity = '0';
            setTimeout(() => {
                if (messageDiv && messageDiv.parentNode) {
                    messageDiv.remove();
                }
            }, 500);
        }
    }, 5000);
}

// Create messages container if it doesn't exist
function createMessagesContainer() {
    const container = document.createElement('div');
    container.id = 'messages';
    container.className = 'fixed top-20 right-4 z-50 max-w-md';
    document.body.appendChild(container);
    return container;
}

// Get message CSS classes based on type
function getMessageClasses(type) {
    const classes = {
        'success': 'bg-green-500 text-white',
        'error': 'bg-red-500 text-white',
        'info': 'bg-blue-500 text-white',
        'warning': 'bg-yellow-500 text-white'
    };
    
    return classes[type] || classes['info'];
}

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimized scroll handler
const optimizedScrollHandler = debounce(updateActiveNavLink, 100);
window.addEventListener('scroll', optimizedScrollHandler);

// Console welcome message
console.log('%c🐕 ONG Resgate de Cães', 'color: #f97316; font-size: 20px; font-weight: bold;');
console.log('%cObrigado por visitar nosso site! Se você é um desenvolvedor e quer ajudar nossa causa, entre em contato!', 'color: #2563eb; font-size: 14px;');
