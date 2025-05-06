from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import UserProfileForm

def api_login_page_view(request):
    """Render login page with form whose submission is handled by JavaScript to call API endpoint"""
    return render(request, 'accounts/api_login_form.html')

def api_register_page_view(request):
    """Render registration page with form whose submission is handled by JavaScript to call API endpoint"""
    return render(request, 'accounts/api_register_form.html')

def logout_view(request):
    """Clear the API token from localStorage (via JS) and log out of Django session"""
    logout(request)
    return render(request, 'accounts/logout.html')

@login_required
def user_profile_view(request):
    """Display and update user profile"""
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'user': user,
        'profile': profile,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)