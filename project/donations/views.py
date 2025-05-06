from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from campaigns.models import Campaign
from .models import Donation
from .forms import DonationForm

def donation_page_view(request, campaign_id):
    """Render donation form page for a campaign (form submitted via JavaScript to API)"""
    campaign = get_object_or_404(Campaign, pk=campaign_id, is_active=True)
    form = DonationForm()
    
    return render(request, 'donations/donation_form.html', {
        'campaign': campaign,
        'form': form,
    })

def donation_success_view(request, donation_id):
    """Display successful donation page"""
    donation = get_object_or_404(Donation, pk=donation_id)
    
    # Security check
    if donation.donor and donation.donor != request.user:
        return redirect('campaigns:campaign_list')
    
    return render(request, 'donations/donation_success.html', {
        'donation': donation,
    })

@login_required
def user_donations_view(request):
    """Display a list of the current user's donations"""
    donations = Donation.objects.filter(donor=request.user).order_by('-created_at')
    
    return render(request, 'donations/user_donations.html', {
        'donations': donations,
    })