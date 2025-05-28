import os
import django
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_analyzer.settings')
django.setup()

def create_superuser():
    User = get_user_model()
    
    # Get superuser credentials from environment variables or use defaults
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'Admin@2024!')
    
    # Check if superuser already exists
    if not User.objects.filter(email=email).exists():
        try:
            User.objects.create_superuser(
                email=email,
                password=password,
                username='admin'
            )
            print(f"Superuser {email} created successfully!")
        except Exception as e:
            print(f"Error creating superuser: {e}")
    else:
        print(f"Superuser {email} already exists.")

if __name__ == '__main__':
    create_superuser() 