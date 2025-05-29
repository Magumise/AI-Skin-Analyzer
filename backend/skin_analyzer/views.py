from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.core.exceptions import ValidationError

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            # Extract data from request
            email = request.data.get('email')
            password = request.data.get('password')
            username = request.data.get('username')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            age = request.data.get('age')
            sex = request.data.get('sex')
            country = request.data.get('country')
            skin_type = request.data.get('skin_type', [])
            skin_concerns = request.data.get('skin_concerns', [])

            # Validate required fields
            if not email:
                return Response(
                    {'error': 'Email is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not password:
                return Response(
                    {'error': 'Password is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not username:
                return Response(
                    {'error': 'Username is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return Response(
                    {'error': 'User with this email already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if User.objects.filter(username=username).exists():
                return Response(
                    {'error': 'Username is already taken'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
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

                # Generate tokens
                refresh = RefreshToken.for_user(user)
                
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
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            ) 