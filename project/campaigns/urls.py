from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('', views.campaign_list_view, name='campaign_list'),
    path('campaigns/<int:pk>/', views.campaign_detail_view, name='campaign_detail'),
    path('campaigns/new/', views.campaign_form_view, name='campaign_create'),
    path('campaigns/<int:pk>/edit/', views.campaign_form_view, name='campaign_edit'),
    path('my-campaigns/', views.user_campaigns_view, name='user_campaigns'),
]