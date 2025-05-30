from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # Use email instead of username

    def validate(self, attrs):
        # Get the email from the request
        email = attrs.get('email')
        password = attrs.get('password')

        # Try to get the user
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