from django.apps import AppConfig
from django.db.models.signals import post_migrate
import logging

logger = logging.getLogger(__name__)

def create_admin_user(sender, **kwargs):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        if not User.objects.filter(email='admin@skincare.com').exists():
            admin = User.objects.create_superuser(
                email='admin@skincare.com',
                password='admin123',
                username='admin',
                is_staff=True,
                is_active=True,
                is_superuser=True
            )
            logger.info('Admin user created successfully!')
            logger.info(f'Admin user details: email={admin.email}, is_staff={admin.is_staff}, is_superuser={admin.is_superuser}')
        else:
            admin = User.objects.get(email='admin@skincare.com')
            # Ensure admin has correct permissions
            if not admin.is_staff or not admin.is_superuser:
                admin.is_staff = True
                admin.is_superuser = True
                admin.save()
                logger.info('Admin permissions updated!')
            logger.info('Admin user already exists')
    except Exception as e:
        logger.error(f'Error creating admin user: {str(e)}')

class SkinAnalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skin_analyzer'

    def ready(self):
        post_migrate.connect(create_admin_user, sender=self) 