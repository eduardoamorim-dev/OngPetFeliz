#!/usr/bin/env python3
"""
Script para corrigir todas as chamadas de API no JavaScript do painel administrativo
"""

import re

# Ler o arquivo JavaScript
with open('static/js/admin_dashboard.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Padrões de substituição para corrigir as chamadas de API
replacements = [
    # Corrigir loadVolunteersData
    (
        r'async loadVolunteersData\(\) \{[^}]*?const response = await fetch\(\'/admin/api/volunteers/\'\);[^}]*?\}',
        '''async loadVolunteersData() {
        try {
            const response = await this.apiRequest('/admin/api/volunteers/');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            const volunteers = await response.json();
            this.renderVolunteersTable(volunteers);
        } catch (error) {
            this.showError('Erro ao carregar voluntários');
        }
    }'''
    ),
    
    # Corrigir loadMessagesData
    (
        r'async loadMessagesData\(\) \{[^}]*?const response = await fetch\(\'/admin/api/messages/\'\);[^}]*?\}',
        '''async loadMessagesData() {
        try {
            const response = await this.apiRequest('/admin/api/messages/');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            const messages = await response.json();
            this.renderMessagesTable(messages);
        } catch (error) {
            this.showError('Erro ao carregar mensagens');
        }
    }'''
    ),
    
    # Corrigir loadTestimonialsData
    (
        r'async loadTestimonialsData\(\) \{[^}]*?const response = await fetch\(\'/admin/api/testimonials/\'\);[^}]*?\}',
        '''async loadTestimonialsData() {
        try {
            const response = await this.apiRequest('/admin/api/testimonials/');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            const testimonials = await response.json();
            this.renderTestimonialsTable(testimonials);
        } catch (error) {
            this.showError('Erro ao carregar depoimentos');
        }
    }'''
    ),
    
    # Corrigir saveDog
    (
        r'const response = await fetch\(\'/admin/api/dogs/\', \{[^}]*?method: \'POST\'[^}]*?\}\);',
        '''const response = await this.apiRequest('/admin/api/dogs/', {
                method: 'POST',
                body: JSON.stringify(dogData)
            });'''
    ),
    
    # Corrigir updateAdoptionStatus
    (
        r'const response = await fetch\(`/admin/api/adoptions/\$\{id\}/`, \{[^}]*?method: \'PATCH\'[^}]*?\}\);',
        '''const response = await this.apiRequest(`/admin/api/adoptions/${id}/`, {
                method: 'PATCH',
                body: JSON.stringify({ status })
            });'''
    ),
    
    # Corrigir updateVolunteerStatus
    (
        r'const response = await fetch\(`/admin/api/volunteers/\$\{id\}/`, \{[^}]*?method: \'PATCH\'[^}]*?\}\);',
        '''const response = await this.apiRequest(`/admin/api/volunteers/${id}/`, {
                method: 'PATCH',
                body: JSON.stringify({ status })
            });'''
    ),
    
    # Corrigir toggleDogFeatured
    (
        r'const response = await fetch\(`/admin/api/dogs/\$\{id\}/toggle-featured/`, \{[^}]*?method: \'POST\'[^}]*?\}\);',
        '''const response = await this.apiRequest(`/admin/api/dogs/${id}/toggle-featured/`, {
                method: 'POST'
            });'''
    ),
    
    # Corrigir toggleTestimonial
    (
        r'const response = await fetch\(`/admin/api/testimonials/\$\{id\}/toggle/`, \{[^}]*?method: \'POST\'[^}]*?\}\);',
        '''const response = await this.apiRequest(`/admin/api/testimonials/${id}/toggle/`, {
                method: 'POST'
            });'''
    )
]

# Aplicar as substituições
for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Salvar o arquivo corrigido
with open('static/js/admin_dashboard.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("JavaScript do painel administrativo corrigido com sucesso!")