from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile(request):
    user_listings = request.user.listings.filter(is_active=True).select_related('game', 'category')
    topup_requests = request.user.topup_requests.all().order_by('-created_at')[:5]
    purchases = request.user.purchases.all().order_by('-created_at')
    return render(request, 'accounts/profile.html', {
        'listings': user_listings,
        'topup_requests': topup_requests,
        'purchases': purchases,
    })

@login_required
def topup(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount and float(amount) > 0:
            from .models import TopUpRequest
            TopUpRequest.objects.create(user=request.user, amount=amount)
            return redirect('profile')
    return render(request, 'accounts/topup.html')
