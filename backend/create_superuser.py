import os
import django
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def create_superuser():
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin@2024!')
        
        try:
            User.objects.create_superuser(
                email=email,
                password=password,
                username='admin'
            )
            print('Superuser created successfully')
        except Exception as e:
            print(f'Error creating superuser: {e}')
    else:
        print('Superuser already exists')

if __name__ == '__main__':
    create_superuser() 