from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sell/', views.create_listing, name='create_listing'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:listing_id>/buy/', views.buy_listing, name='buy_listing'),
    path('order/<int:order_id>/confirm/', views.confirm_order, name='confirm_order'),
]
