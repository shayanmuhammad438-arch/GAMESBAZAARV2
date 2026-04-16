from django.contrib import admin
from .models import Category, Game, Listing, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    search_fields = ('name',)
    filter_horizontal = ('categories',)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'game', 'category', 'seller', 'price', 'is_active')
    list_filter = ('game', 'category', 'is_active')
    search_fields = ('title', 'description', 'seller__username')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'seller', 'price', 'commission_amount', 'seller_amount', 'status', 'created_at')
    list_filter = ('status',)
