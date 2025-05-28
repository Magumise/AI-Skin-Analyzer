from django.shortcuts import render
import requests
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, UploadedImage, AnalysisResult, Product, Appointment
from .serializers import (
    UserSerializer, UploadedImageSerializer, AnalysisResultSerializer,
    ProductSerializer, AppointmentSerializer
)

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Allow registration and listing without authentication
        """
        if self.action in ['create', 'list']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = User.objects.all()
        # Add the last skin condition for each user
        for user in queryset:
            last_analysis = AnalysisResult.objects.filter(user=user).order_by('-timestamp').first()
            if last_analysis:
                user.last_skin_condition = last_analysis.condition
            else:
                user.last_skin_condition = 'No analysis yet'
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Custom create method for user registration
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': serializer.data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Custom update method to handle user updates
        """
        instance = self.get_object()
        # Only allow users to update their own profile
        if instance != request.user:
            return Response(
                {'error': 'You can only update your own profile'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method to handle user deletion
        """
        instance = self.get_object()
        # Only allow users to delete their own account
        if instance != request.user:
            return Response(
                {'error': 'You can only delete your own account'},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UploadedImageViewSet(viewsets.ModelViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        image = self.get_object()
        
        try:
            # Get analysis results from request data
            analysis_data = request.data
            
            # Validate required fields
            required_fields = ['condition', 'confidence', 'recommendation_type']
            for field in required_fields:
                if field not in analysis_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Create analysis result
            analysis = AnalysisResult.objects.create(
                image=image,
                user=request.user,
                condition=analysis_data['condition'],
                confidence=analysis_data['confidence'],
                recommendation_type=analysis_data['recommendation_type'],
                message=analysis_data.get('message', '')
            )
            
            # If products are recommended, fetch them from our database
            if 'recommendations' in analysis_data:
                # Extract product names from recommendations
                product_names = [r.get('Product', '') for r in analysis_data['recommendations']]
                # Filter out empty strings
                product_names = [name for name in product_names if name]
                
                if product_names:
                    # Get products from database that match the recommended names
                    products = Product.objects.filter(name__in=product_names)
                    
                    # Get the condition from the AI response
                    condition = analysis_data['condition'].lower()
                    
                    # Filter products based on the condition
                    filtered_products = []
                    for product in products:
                        # Check if the product's targets or suitable_for contains the condition
                        if (condition in product.targets.lower() or 
                            condition in product.suitable_for.lower()):
                            filtered_products.append(product)
                    
                    # Serialize the filtered products
                    product_data = ProductSerializer(filtered_products, many=True, context={'request': request}).data
                    
                    # Include only the filtered products in the response
                    analysis_data['products'] = product_data
                    # Remove the original recommendations since we're using our database products
                    analysis_data.pop('recommendations', None)
            
            return Response(analysis_data)
            
        except ValueError as ve:
            print(f"Validation error: {str(ve)}")
            return Response(
                {'error': str(ve)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"Error processing analysis: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'update_image']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # Remove image from data if it's not a file
            if 'image' in request.data and not isinstance(request.data['image'], (str, type(None))):
                request.data.pop('image')
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def update_image(self, request, pk=None):
        try:
            product = self.get_object()
            if 'image' not in request.FILES:
                return Response(
                    {'error': 'No image file provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            product.image = request.FILES['image']
            product.save()
            
            serializer = self.get_serializer(product)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=self.request.user)
