from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from app.models import Article, Category
import random

class Command(BaseCommand):
    help = 'Generates fake news articles for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--articles',
            type=int,
            default=10,
            help='The number of fake articles to create'
        )
        parser.add_argument(
            '--categories',
            type=int,
            default=5,
            help='The number of categories to create'
        )

    def handle(self, *args, **options):
        fake = Faker()
        num_articles = options['articles']
        num_categories = options['categories']

        # Create categories if they don't exist
        categories = []
        category_names = [
            'Politics', 'Technology', 'Sports', 'Entertainment', 
            'Business', 'Health', 'Science', 'Education', 
            'World News', 'Local News'
        ]

        self.stdout.write('Creating categories...')
        for i in range(min(num_categories, len(category_names))):
            name = category_names[i]
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name)}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {name}')

        # Create fake articles
        self.stdout.write('Creating fake articles...')
        locations = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 
                    'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']

        for _ in range(num_articles):
            title = fake.catch_phrase()
            
            # Generate a longer, more news-like content
            paragraphs = [
                fake.paragraph(nb_sentences=8),
                fake.paragraph(nb_sentences=6),
                fake.paragraph(nb_sentences=7),
                '\n\n',
                f'Reporting from {random.choice(locations)},',
                fake.name()
            ]
            content = '\n\n'.join(paragraphs)

            article = Article.objects.create(
                title=title,
                content=content,
                is_published=random.choice([True, True, True, False]),  # 75% chance of being published
                author=fake.name(),
                category=random.choice(categories),
                location=random.choice(locations)
            )
            self.stdout.write(f'Created article: {article.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {num_articles} fake articles in {num_categories} categories'
            )
        )
