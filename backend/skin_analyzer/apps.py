from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_admin_user(sender, **kwargs):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(email='admin@skincare.com').exists():
        User.objects.create_superuser(
            email='admin@skincare.com',
            password='admin123',
            username='admin',
            is_staff=True,
            is_active=True,
            role='ADMIN'
        )
        print('Admin user created successfully!')
    else:
        print('Admin user already exists')

class SkinAnalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skin_analyzer'

    def ready(self):
        post_migrate.connect(create_admin_user, sender=self) 