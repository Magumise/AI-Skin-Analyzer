import os
import django
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def create_deployed_admin():
    User = get_user_model()
    
    # Admin credentials
    email = 'admin@skincare.com'
    password = 'admin123'
    
    try:
        # Check if admin user exists
        admin = User.objects.filter(email=email).first()
        
        if admin:
            print(f"Admin user {email} already exists")
            # Update permissions if needed
            if not admin.is_staff or not admin.is_superuser:
                admin.is_staff = True
                admin.is_superuser = True
                admin.is_active = True
                admin.save()
                print("Updated admin permissions")
        else:
            # Create new admin user
            admin = User.objects.create_superuser(
                email=email,
                password=password,
                username='admin',
                is_staff=True,
                is_active=True,
                is_superuser=True
            )
            print(f"Created admin user {email}")
        
        # Verify the user can be authenticated
        if admin.check_password(password):
            print("Password verification successful")
        else:
            print("Warning: Password verification failed")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    create_deployed_admin() 