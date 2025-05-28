from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserViewSet, UploadedImageViewSet, ProductViewSet, AppointmentViewSet,
    EmailTokenObtainPairView, RegisterView
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'images', UploadedImageViewSet, basename='image')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

# The API URLs are now determined automatically by the router
urlpatterns = [
    # Registration endpoint FIRST
    path('users/register/', RegisterView.as_view(), name='user-register'),

    # Include the router URLs
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Add a test endpoint
    path('test/', UserViewSet.as_view({'get': 'test'}), name='test'),
] 