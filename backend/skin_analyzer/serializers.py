from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # Use email instead of username

    def validate(self, attrs):
        # Get the email from the request
        email = attrs.get('email')
        password = attrs.get('password')

        # Special case for admin login
        if email == 'admin@skincare.com' and password == 'admin123':
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create admin user if it doesn't exist
                user = User.objects.create_superuser(
                    email=email,
                    password=password,
                    username='admin'
                )
            
            # Ensure user has admin privileges
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()

            # Generate tokens
            refresh = self.get_token(user)
            data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                }
            }
            return data

        # For all other users, proceed with normal authentication
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise self.get_error_messages()['no_active_account']

        # Check if user is staff or superuser
        if not (user.is_staff or user.is_superuser):
            raise self.get_error_messages()['no_active_account']

        # Validate credentials
        if not user.check_password(password):
            raise self.get_error_messages()['no_active_account']

        # Generate tokens
        refresh = self.get_token(user)
        data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser
            }
        }
        return data 

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    image = serializers.ImageField(required=False)
    suitable_for = serializers.CharField(required=False)
    targets = serializers.CharField(required=False)
    when_to_apply = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'image', 'suitable_for', 'targets', 'when_to_apply', 'price', 'category', 'brand', 'stock')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Convert string fields to arrays for frontend
        if isinstance(data['suitable_for'], str):
            data['suitable_for'] = [item.strip() for item in data['suitable_for'].split(',') if item.strip()]
        if isinstance(data['targets'], str):
            data['targets'] = [item.strip() for item in data['targets'].split(',') if item.strip()]
        if isinstance(data['when_to_apply'], str):
            data['when_to_apply'] = [item.strip() for item in data['when_to_apply'].split(',') if item.strip()]
        return data

    def to_internal_value(self, data):
        # Convert array fields to strings for database
        if 'suitable_for' in data and isinstance(data['suitable_for'], list):
            data['suitable_for'] = ', '.join(data['suitable_for'])
        if 'targets' in data and isinstance(data['targets'], list):
            data['targets'] = ', '.join(data['targets'])
        if 'when_to_apply' in data and isinstance(data['when_to_apply'], list):
            data['when_to_apply'] = ', '.join(data['when_to_apply'])
        return super().to_internal_value(data) 