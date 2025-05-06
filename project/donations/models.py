from django.db import models
from django.contrib.auth.models import User
from campaigns.models import Campaign

class Donation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donations')
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    anonymous = models.BooleanField(default=False)
    simulated_payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"${self.amount} to {self.campaign.title}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Update campaign current_amount when donation is completed
        if self.simulated_payment_status == 'completed':
            if is_new:  # Only update on new completed donations
                self.campaign.current_amount += self.amount
                self.campaign.save()