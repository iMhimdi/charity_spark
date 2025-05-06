"""
URL configuration for charity_spark_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('campaigns.urls')),
    path('accounts/', include('accounts.urls')),
    path('donations/', include('donations.urls')),
    path('api/', include('api.urls')),
    
    # Static pages
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('impact/', TemplateView.as_view(template_name='pages/impact.html'), name='impact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)