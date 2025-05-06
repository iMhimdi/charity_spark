from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('campaign/<int:campaign_id>/donate/', views.donation_page_view, name='donation_form'),
    path('success/<int:donation_id>/', views.donation_success_view, name='donation_success'),
    path('my-donations/', views.user_donations_view, name='user_donations'),
]