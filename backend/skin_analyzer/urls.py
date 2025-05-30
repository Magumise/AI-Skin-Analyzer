from django.urls import path, include
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    UserRegistrationView,
    CustomTokenObtainPairView,
    create_admin_user,
    add_all_products,
    UserViewSet,
    ProductViewSet,
    UploadedImageViewSet,
    AnalysisResultViewSet,
    AppointmentViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'images', UploadedImageViewSet, basename='image')
router.register(r'analysis', AnalysisResultViewSet, basename='analysis')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
    
    # Test route to verify URL routing
    path('test/', lambda request: JsonResponse({'message': 'Routing works'}), name='test_route'),
    
    # JWT authentication routes
    path('users/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/register/', UserRegistrationView.as_view(), name='user_register'),
    path('users/create-admin/', create_admin_user, name='create_admin_user'),
    path('products/add-all/', add_all_products, name='add-all-products'),
] 