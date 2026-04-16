from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="e.g. 15.00 for 15%")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji or icon shorthand, e.g., 🎮")
    categories = models.ManyToManyField(Category, related_name='games', blank=True)

    def __str__(self):
        return self.name

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Listing(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        null=True, 
        blank=True,
        help_text="Leave empty for an evergreen/infinite listing. Otherwise, set a quantity between 1 and 999."
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.price}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, related_name='orders')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total price paid by buyer")
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    seller_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Amount seller receives")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.listing.title if self.listing else 'Deleted Listing'}"
