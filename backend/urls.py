"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # API Documentation
    path('', include_docs_urls(
        title='AI Skin Analyzer API',
        description='API documentation for AI Skin Analyzer',
        permission_classes=[AllowAny]
    )),
    path('schema/', get_schema_view(
        title='AI Skin Analyzer API Schema',
        description='API schema for AI Skin Analyzer',
        permission_classes=[AllowAny]
    )),
    
    # JWT Authentication Routes (temporarily added here for testing)
    path('api/users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # API Endpoints
    path('api/', include('skin_analyzer.urls')),
    
    # Admin Interface
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
