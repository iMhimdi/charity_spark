from django.contrib import admin
from .models import Category, Campaign

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'category', 'goal_amount', 'current_amount', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'creator__username')
    readonly_fields = ('current_amount',)