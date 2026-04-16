from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Game, Listing, Order
from .forms import ListingForm

def home(request):
    games = Game.objects.prefetch_related('categories').all()
    return render(request, 'core/home.html', {'games': games})

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            messages.success(request, 'Listing created successfully!')
            return redirect('home')
    else:
        form = ListingForm()
    return render(request, 'core/create_listing.html', {'form': form})

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    # Get active listings for this game
    listings = game.listings.filter(is_active=True).select_related('seller', 'category')
    return render(request, 'core/game_detail.html', {'game': game, 'listings': listings})

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, is_active=True)
    return render(request, 'core/listing_detail.html', {'listing': listing})

from decimal import Decimal

@login_required
def buy_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, is_active=True)
    
    if request.method == 'POST':
        if listing.seller == request.user:
            messages.error(request, "You can't buy your own listing!")
            return redirect('listing_detail', listing_id=listing.id)

        if request.user.balance < listing.price:
            messages.error(request, "Insufficient wallet balance. Please top up.")
            return redirect('listing_detail', listing_id=listing.id)

        # Calculate commission
        fee_pct = listing.category.commission_percentage
        commission = (listing.price * fee_pct) / Decimal('100.00')
        seller_amount = listing.price - commission

        # Deduct balance
        request.user.balance -= listing.price
        request.user.save()

        # Create Order (Escrow)
        Order.objects.create(
            listing=listing,
            buyer=request.user,
            seller=listing.seller,
            price=listing.price,
            commission_amount=commission,
            seller_amount=seller_amount,
            status='processing'
        )

        # Mark listing as inactive
        listing.is_active = False
        listing.save()

        messages.success(request, "Purchase successful! The order is now processing.")
        return redirect('profile')
    
    return redirect('listing_detail', listing_id=listing.id)

@login_required
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user, status='processing')
    if request.method == 'POST':
        # Complete order
        order.status = 'completed'
        order.save()

        # Transfer funds to seller (minus commission)
        seller = order.seller
        seller.balance += order.seller_amount
        seller.save()
        
        messages.success(request, "Order confirmed! Funds have been released to the seller.")
    return redirect('profile')
