from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'campaigns', views.CampaignViewSet)
router.register(r'donations', views.DonationViewSet)

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('auth/login/', views.LoginAPIView.as_view(), name='api_login'),
    path('auth/user/', views.UserAPIView.as_view(), name='api_user'),
    
    # Include the router URLs
    path('', include(router.urls)),
    
    # DRF browsable API login/logout
    path('auth/', include('rest_framework.urls')),
]