from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from .models import Campaign, Category
from .forms import CampaignForm

def campaign_list_view(request):
    """Display list of campaigns with filtering options"""
    categories = Category.objects.all()
    campaigns = Campaign.objects.filter(is_active=True).order_by('-created_at')
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        campaigns = campaigns.filter(category_id=category_id)
    
    # Filter by search query
    query = request.GET.get('q')
    if query:
        campaigns = campaigns.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Featured campaigns
    featured_campaigns = Campaign.objects.filter(is_featured=True, is_active=True)[:3]
    
    # Pagination
    paginator = Paginator(campaigns, 9)  # 9 campaigns per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'featured_campaigns': featured_campaigns,
        'categories': categories,
        'selected_category': category_id,
        'query': query,
    }
    return render(request, 'campaigns/campaign_list.html', context)

def campaign_detail_view(request, pk):
    """Display details of a specific campaign"""
    campaign = get_object_or_404(Campaign, pk=pk)
    
    # Get related campaigns (same category)
    related_campaigns = Campaign.objects.filter(
        category=campaign.category, 
        is_active=True
    ).exclude(id=campaign.id)[:3]
    
    context = {
        'campaign': campaign,
        'related_campaigns': related_campaigns,
    }
    return render(request, 'campaigns/campaign_detail.html', context)

@login_required
def campaign_form_view(request, pk=None):
    """Create or edit a campaign"""
    # This view renders the form, but submission will be handled by JavaScript to API
    if pk:
        campaign = get_object_or_404(Campaign, pk=pk)
        if campaign.creator != request.user:
            return redirect('campaigns:campaign_list')
    else:
        campaign = None
    
    form = CampaignForm(instance=campaign)
    
    context = {
        'form': form,
        'campaign': campaign,
    }
    return render(request, 'campaigns/campaign_form.html', context)

@login_required
def user_campaigns_view(request):
    """Display the current user's campaigns"""
    campaigns = Campaign.objects.filter(creator=request.user).order_by('-created_at')
    
    # Stats
    total_raised = campaigns.aggregate(Sum('current_amount'))['current_amount__sum'] or 0
    active_campaigns = campaigns.filter(is_active=True).count()
    
    context = {
        'campaigns': campaigns,
        'total_raised': total_raised,
        'active_campaigns': active_campaigns,
    }
    return render(request, 'campaigns/user_campaigns.html', context)