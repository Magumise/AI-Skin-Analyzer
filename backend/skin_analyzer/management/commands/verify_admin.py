from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

User = get_user_model()

class Command(BaseCommand):
    help = 'Verifies the admin user exists and has correct permissions'

    def handle(self, *args, **options):
        try:
            # Check if admin user exists
            admin = User.objects.filter(email='admin@skincare.com').first()
            
            if not admin:
                self.stdout.write(self.style.ERROR('Admin user does not exist!'))
                # Create admin user
                admin = User.objects.create_superuser(
                    email='admin@skincare.com',
                    password='admin123',
                    username='admin',
                    is_staff=True,
                    is_active=True
                )
                self.stdout.write(self.style.SUCCESS('Admin user created successfully!'))
            else:
                self.stdout.write(self.style.SUCCESS('Admin user exists!'))
            
            # Verify admin permissions
            if not admin.is_staff:
                admin.is_staff = True
                admin.save()
                self.stdout.write(self.style.SUCCESS('Admin user granted staff permissions!'))
            
            if not admin.is_superuser:
                admin.is_superuser = True
                admin.save()
                self.stdout.write(self.style.SUCCESS('Admin user granted superuser permissions!'))
            
            # Verify email
            try:
                validate_email(admin.email)
                self.stdout.write(self.style.SUCCESS('Admin email is valid!'))
            except ValidationError:
                self.stdout.write(self.style.ERROR('Admin email is invalid!'))
            
            # Print admin details
            self.stdout.write(self.style.SUCCESS(f'''
Admin user details:
- Email: {admin.email}
- Username: {admin.username}
- Is Staff: {admin.is_staff}
- Is Superuser: {admin.is_superuser}
- Is Active: {admin.is_active}
'''))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}')) 