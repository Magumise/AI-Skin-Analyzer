from django.urls import path
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    UserRegistrationView,
    CustomTokenObtainPairView,
    create_admin_user,
    add_all_products
)

urlpatterns = [
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