from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser with the specified credentials'

    def handle(self, *args, **options):
        if not User.objects.filter(email='admin@skincare.com').exists():
            User.objects.create_superuser(
                email='admin@skincare.com',
                password='admin123',
                username='admin',
                is_staff=True,
                is_active=True,
                role='ADMIN'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists')) 