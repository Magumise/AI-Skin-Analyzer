from django.urls import path
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import UserRegistrationView

urlpatterns = [
    # Test route to verify URL routing
    path('test/', lambda request: JsonResponse({'message': 'Routing works'}), name='test_route'),
    
    # JWT authentication routes
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/register/', UserRegistrationView.as_view(), name='user_register'),
] 