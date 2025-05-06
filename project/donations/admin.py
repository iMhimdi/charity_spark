from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'donor', 'amount', 'simulated_payment_status', 'created_at')
    list_filter = ('simulated_payment_status', 'created_at')
    search_fields = ('campaign__title', 'donor__username', 'message')
    readonly_fields = ('created_at',)