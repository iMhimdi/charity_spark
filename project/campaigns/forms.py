from django import forms
from .models import Campaign

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'category', 'goal_amount', 'image', 'end_date']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }