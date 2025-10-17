"""
URL Configuration for messaging_app project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from chats.views import ConversationViewSet, MessageViewSet, UserViewSet
from chats.auth import CustomTokenObtainPairView, register_user, user_profile

# Create router and register viewsets
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', register_user, name='register'),
    path('api/auth/profile/', user_profile, name='user_profile'),
    
    # API endpoints
    path('api/', include(router.urls)),
    
    # DRF browsable API (optional, for development)
    path('api-auth/', include('rest_framework.urls')),
]