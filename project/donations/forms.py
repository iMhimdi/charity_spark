from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'message', 'anonymous']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': 1, 'step': 0.01}),
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a supportive message (optional)'}),
        }