from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Product, UploadedImage, AnalysisResult, Appointment
from .serializers import CustomTokenObtainPairSerializer, ProductSerializer, UserSerializer, UploadedImageSerializer, AnalysisResultSerializer, AppointmentSerializer
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError
import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import permissions

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

@api_view(['POST'])
@permission_classes([AllowAny])
def create_admin_user(request):
    User = get_user_model()
    
    # Admin credentials
    email = 'admin@skincare.com'
    password = 'admin123'
    
    try:
        # Check if admin user exists
        admin = User.objects.filter(email=email).first()
        
        if admin:
            # Update permissions if needed
            if not admin.is_staff or not admin.is_superuser:
                admin.is_staff = True
                admin.is_superuser = True
                admin.is_active = True
                admin.save()
                return Response({'message': 'Admin permissions updated'})
            return Response({'message': 'Admin user already exists'})
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
            return Response({'message': 'Admin user created successfully'})
            
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_all_products(request):
    products = [
        {
            'name': 'Botanical Repair Mist',
            'brand': 'Aurora Beauty',
            'category': 'Toner',
            'description': 'A soothing mist that helps repair and rejuvenate skin.',
            'price': 24.99,
            'stock': 50,
            'suitable_for': 'Acne, Eczema, Rosacea, Dry Skin, Normal Skin',
            'targets': 'Skin Repair, Hydration, Soothing',
            'when_to_apply': 'AM/PM'
        },
        {
            'name': 'Lavender Foaming Face Wash',
            'brand': 'Aurora Beauty',
            'category': 'Cleanser',
            'description': 'Gentle foaming cleanser with lavender extract.',
            'price': 19.99,
            'stock': 45,
            'suitable_for': 'Acne, Rosacea, Oily Skin',
            'targets': 'Cleansing, Oil Control',
            'when_to_apply': 'AM/PM'
        },
        {
            'name': 'Sandal Mist',
            'brand': 'Aurora Beauty',
            'category': 'Toner',
            'description': 'Refreshing mist with sandalwood extract.',
            'price': 22.99,
            'stock': 40,
            'suitable_for': 'Acne, Rosacea, Dry Skin, Normal Skin',
            'targets': 'Hydration, Soothing',
            'when_to_apply': 'AM/PM'
        },
        {
            'name': 'BIO Enzyme GLYCOLIC Vinegar',
            'brand': 'Aurora Beauty',
            'category': 'Treatment',
            'description': 'Exfoliating treatment with glycolic acid.',
            'price': 29.99,
            'stock': 35,
            'suitable_for': 'Acne, Keratosis, Milia, Oily Skin',
            'targets': 'Exfoliation, Brightening',
            'when_to_apply': 'PM'
        },
        {
            'name': 'Asian Clay & Rose Mask',
            'brand': 'Aurora Beauty',
            'category': 'Mask',
            'description': 'Purifying clay mask with rose extract.',
            'price': 27.99,
            'stock': 30,
            'suitable_for': 'Acne, Wrinkles, Oily Skin, Normal Skin',
            'targets': 'Deep Cleansing, Anti-aging',
            'when_to_apply': 'PM'
        },
        {
            'name': 'Intensive Skin Repair Sandal Lotion',
            'brand': 'Aurora Beauty',
            'category': 'Moisturizer',
            'description': 'Intensive repair lotion with sandalwood.',
            'price': 34.99,
            'stock': 40,
            'suitable_for': 'Acne, Eczema, Rosacea, Wrinkles, Dry Skin',
            'targets': 'Skin Repair, Moisturizing',
            'when_to_apply': 'AM/PM'
        },
        {
            'name': 'Niacinamide & NEEM Toner',
            'brand': 'Aurora Beauty',
            'category': 'Toner',
            'description': 'Balancing toner with niacinamide and neem.',
            'price': 21.99,
            'stock': 45,
            'suitable_for': 'Acne, Rosacea, Oily Skin, Hyperpigmentation',
            'targets': 'Oil Control, Brightening',
            'when_to_apply': 'AM/PM'
        },
        {
            'name': 'Charcoal Detox Soap',
            'brand': 'Aurora Beauty',
            'category': 'Cleanser',
            'description': 'Deep cleansing soap with activated charcoal.',
            'price': 16.99,
            'stock': 50,
            'suitable_for': 'Acne, Oily Skin',
            'targets': 'Deep Cleansing, Detoxifying',
            'when_to_apply': 'AM/PM'
        },
        {
            'name': 'Lavender Soothing Lotion',
            'brand': 'Aurora Beauty',
            'category': 'Moisturizer',
            'description': 'Calming lotion with lavender extract.',
            'price': 29.99,
            'stock': 40,
            'suitable_for': 'Eczema, Rosacea, Dry Skin',
            'targets': 'Soothing, Moisturizing',
            'when_to_apply': 'AM/PM'
        },
        {
            'name': 'Radiant Plump Serum',
            'brand': 'Aurora Beauty',
            'category': 'Serum',
            'description': 'Hydrating serum for plump, radiant skin.',
            'price': 39.99,
            'stock': 35,
            'suitable_for': 'Eczema, Rosacea, Wrinkles, Dry Skin, Hyperpigmentation',
            'targets': 'Hydration, Anti-aging',
            'when_to_apply': 'AM/PM'
        },
        {
            'name': 'Radiant Rose Face Mist',
            'brand': 'Aurora Beauty',
            'category': 'Toner',
            'description': 'Refreshing rose mist for radiant skin.',
            'price': 23.99,
            'stock': 45,
            'suitable_for': 'Eczema, Rosacea, Dry Skin, Normal Skin',
            'targets': 'Hydration, Brightening',
            'when_to_apply': 'AM/PM'
        },
        {
            'name': 'Radiant Plump Moisturizer with Glutathione',
            'brand': 'Aurora Beauty',
            'category': 'Moisturizer',
            'description': 'Advanced moisturizer with glutathione for radiant skin.',
            'price': 44.99,
            'stock': 30,
            'suitable_for': 'Eczema, Rosacea, Wrinkles, Dry Skin, Hyperpigmentation',
            'targets': 'Anti-aging, Brightening',
            'when_to_apply': 'AM/PM'
        },
        {
            'name': 'Sandal Glow Facial & Body Scrub',
            'brand': 'Aurora Beauty',
            'category': 'Scrub',
            'description': 'Exfoliating scrub with sandalwood for glowing skin.',
            'price': 26.99,
            'stock': 35,
            'suitable_for': 'Keratosis, Wrinkles, Dry Skin',
            'targets': 'Exfoliation, Brightening',
            'when_to_apply': 'PM'
        }
    ]

    created_products = []
    for product_data in products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        created_products.append(product)

    serializer = ProductSerializer(created_products, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        # Temporarily allow any user to access all product actions
        return [permissions.AllowAny()]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_permissions(self):
        # Temporarily allow any user to access all user actions
        return [permissions.AllowAny()]

# Assuming UploadedImageViewSet and AppointmentViewSet also exist and need similar temporary permission adjustments
# If you encounter 401 errors on image or appointment endpoints, we may need to adjust them as well.

class UploadedImageViewSet(viewsets.ModelViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        # Temporarily allow any user to access all image actions
        return [permissions.AllowAny()]

class AnalysisResultViewSet(viewsets.ModelViewSet):
    queryset = AnalysisResult.objects.all()
    serializer_class = AnalysisResultSerializer

    def get_permissions(self):
        # Temporarily allow any user to access all analysis result actions
        return [permissions.AllowAny()]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    
    def get_permissions(self):
        # Temporarily allow any user to access all appointment actions
        return [permissions.AllowAny()] 