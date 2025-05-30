from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import CustomTokenObtainPairSerializer
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError
import logging

logger = logging.getLogger(__name__)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            logger.info("Login successful")
            return response
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            logger.info(f"Registration attempt with data: {request.data}")
            
            # Extract data from request
            email = request.data.get('email', '').strip()
            password = request.data.get('password')
            username = request.data.get('username', '').strip()
            first_name = request.data.get('first_name', '').strip()
            last_name = request.data.get('last_name', '').strip()
            age = request.data.get('age')
            sex = request.data.get('sex')
            country = request.data.get('country')
            skin_type = request.data.get('skin_type', [])
            skin_concerns = request.data.get('skin_concerns', [])

            logger.info(f"Processed registration data: email={email}, username={username}")

            # Validate email format
            try:
                validate_email(email)
                logger.info("Email validation passed")
            except DjangoValidationError as e:
                logger.error(f"Email validation failed: {str(e)}")
                return Response(
                    {'email': ['Please enter a valid email address.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate required fields
            if not email:
                logger.error("Email is missing")
                return Response(
                    {'email': ['Email is required.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not password:
                logger.error("Password is missing")
                return Response(
                    {'password': ['Password is required.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not username:
                logger.error("Username is missing")
                return Response(
                    {'username': ['Username is required.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if user already exists
            if User.objects.filter(email=email).exists():
                logger.error(f"User with email {email} already exists")
                return Response(
                    {'email': ['A user with this email already exists.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if User.objects.filter(username=username).exists():
                logger.error(f"Username {username} is already taken")
                return Response(
                    {'username': ['This username is already taken.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                logger.info("Attempting to create user")
                # Create user
                user = User.objects.create_user(
                    email=email,
                    username=username,
                    password=password,
                    first_name=first_name or '',
                    last_name=last_name or ''
                )

                # Add additional fields
                if age:
                    user.age = age
                if sex:
                    user.sex = sex
                if country:
                    user.country = country
                if skin_type:
                    user.skin_type = skin_type
                if skin_concerns:
                    user.skin_concerns = skin_concerns

                user.save()
                logger.info(f"User created successfully: {user.email}")

                # Generate tokens
                refresh = RefreshToken.for_user(user)
                logger.info("Tokens generated successfully")
                
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                }, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                logger.error(f"Validation error during user creation: {str(e)}")
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error(f"Unexpected error during registration: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            ) 