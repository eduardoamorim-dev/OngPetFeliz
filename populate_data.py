#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogs_rescue.settings')
django.setup()

from main.models import Dog, Testimonial

# Create sample dogs
dogs_data = [
    {
        'name': 'Luna',
        'age': 2,
        'gender': 'F',
        'size': 'M',
        'breed': 'Labrador Mix',
        'description': 'Luna é uma cadela muito carinhosa e brincalhona. Adora crianças e se dá bem com outros animais. Está procurando uma família que possa dar muito amor e atenção.',
        'personality': 'Carinhosa, brincalhona, obediente',
        'photo_url': 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=500&h=400&fit=crop',
        'is_featured': True,
        'status': 'available'
    },
    {
        'name': 'Max',
        'age': 4,
        'gender': 'M',
        'size': 'G',
        'breed': 'Pastor Alemão Mix',
        'description': 'Max é um cão protetor e leal. Já foi treinado e é muito obediente. Precisa de uma família com experiência em cães grandes.',
        'personality': 'Protetor, leal, inteligente',
        'photo_url': 'https://images.unsplash.com/photo-1551717743-49959800b1f6?w=500&h=400&fit=crop',
        'is_featured': True,
        'status': 'available'
    },
    {
        'name': 'Bella',
        'age': 1,
        'gender': 'F',
        'size': 'P',
        'breed': 'Poodle Mix',
        'description': 'Bella é uma jovem cadela cheia de energia. Adora brincar e fazer novos amigos. Perfeita para apartamentos.',
        'personality': 'Energética, amigável, pequena',
        'photo_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=500&h=400&fit=crop',
        'is_featured': True,
        'status': 'available'
    },
    {
        'name': 'Rocky',
        'age': 5,
        'gender': 'M',
        'size': 'M',
        'breed': 'Bulldog Mix',
        'description': 'Rocky é um cão calmo e afetuoso. Ideal para famílias que buscam um companheiro tranquilo e fiel.',
        'personality': 'Calmo, afetuoso, companheiro',
        'photo_url': 'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=500&h=400&fit=crop',
        'is_featured': False,
        'status': 'available'
    },
    {
        'name': 'Nina',
        'age': 3,
        'gender': 'F',
        'size': 'M',
        'breed': 'Border Collie Mix',
        'description': 'Nina é muito inteligente e ativa. Precisa de bastante exercício e estímulo mental. Ideal para famílias ativas.',
        'personality': 'Inteligente, ativa, obediente',
        'photo_url': 'https://images.unsplash.com/photo-1581888227599-779811939961?w=500&h=400&fit=crop',
        'is_featured': False,
        'status': 'available'
    },
    {
        'name': 'Thor',
        'age': 6,
        'gender': 'M',
        'size': 'G',
        'breed': 'Rottweiler Mix',
        'description': 'Thor é um cão maduro e equilibrado. Muito protetor com a família, mas carinhoso. Precisa de um tutor experiente.',
        'personality': 'Protetor, equilibrado, carinhoso',
        'photo_url': 'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=500&h=400&fit=crop',
        'is_featured': True,
        'status': 'available'
    }
]

# Create testimonials
testimonials_data = [
    {
        'adopter_name': 'Maria Silva',
        'dog_name': 'Bobby',
        'testimonial': 'Adotar o Bobby foi a melhor decisão que tomamos! Ele trouxe tanto amor e alegria para nossa família. A ONG nos deu todo o suporte necessário durante o processo.',
        'photo_after_url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=150&h=150&fit=crop&crop=face',
        'is_active': True
    },
    {
        'adopter_name': 'João Santos',
        'dog_name': 'Mel',
        'testimonial': 'A Mel se adaptou perfeitamente à nossa rotina. É incrível como ela já sabia que estava em casa. Recomendo muito a adoção responsável!',
        'photo_after_url': 'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=150&h=150&fit=crop&crop=face',
        'is_active': True
    },
    {
        'adopter_name': 'Ana Costa',
        'dog_name': 'Rex',
        'testimonial': 'O Rex chegou em nossa vida no momento perfeito. Ele é nosso companheiro fiel e trouxe muita felicidade para todos nós.',
        'photo_after_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=150&h=150&fit=crop&crop=face',
        'is_active': True
    },
    {
        'adopter_name': 'Carlos Oliveira',
        'dog_name': 'Luna',
        'testimonial': 'Nossa Luna é simplesmente perfeita! O processo de adoção foi muito bem organizado e a equipe sempre muito atenciosa.',
        'photo_after_url': 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=150&h=150&fit=crop&crop=face',
        'is_active': True
    }
]

def populate_database():
    print("Populating database with sample data...")
    
    # Clear existing data
    Dog.objects.all().delete()
    Testimonial.objects.all().delete()
    
    # Create dogs
    dogs_created = 0
    for dog_data in dogs_data:
        dog, created = Dog.objects.get_or_create(
            name=dog_data['name'],
            defaults=dog_data
        )
        if created:
            dogs_created += 1
            print(f"Created dog: {dog.name}")
    
    # Create testimonials
    testimonials_created = 0
    for testimonial_data in testimonials_data:
        testimonial, created = Testimonial.objects.get_or_create(
            adopter_name=testimonial_data['adopter_name'],
            dog_name=testimonial_data['dog_name'],
            defaults=testimonial_data
        )
        if created:
            testimonials_created += 1
            print(f"Created testimonial by: {testimonial.adopter_name}")
    
    print(f"\nDatabase populated successfully!")
    print(f"- {dogs_created} dogs created")
    print(f"- {testimonials_created} testimonials created")
    print(f"- Total dogs available: {Dog.objects.filter(status='available').count()}")
    print(f"- Featured dogs: {Dog.objects.filter(is_featured=True).count()}")

if __name__ == '__main__':
    populate_database()