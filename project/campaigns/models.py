from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Campaign(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='campaigns')
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='campaign_images/', blank=True, null=True)
    end_date = models.DateField()
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('campaigns:campaign_detail', args=[str(self.id)])
    
    @property
    def progress_percentage(self):
        if float(self.goal_amount) == 0:
            return 0
        return int((float(self.current_amount) / float(self.goal_amount)) * 100)
    
    @property
    def is_completed(self):
        return float(self.current_amount) >= float(self.goal_amount)
    
    @property
    def days_remaining(self):
        from datetime import date
        delta = self.end_date - date.today()
        return max(0, delta.days)