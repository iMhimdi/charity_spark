from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.api_login_page_view, name='api_login_page'),
    path('register/', views.api_register_page_view, name='api_register_page'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile_view, name='profile'),
]