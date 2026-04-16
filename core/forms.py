from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['game', 'category', 'title', 'price', 'quantity', 'description']

    def clean(self):
        cleaned_data = super().clean()
        game = cleaned_data.get("game")
        category = cleaned_data.get("category")

        if game and category:
            if category not in game.categories.all():
                raise forms.ValidationError({
                    'category': f"{category.name} is not available for {game.name}."
                })
        return cleaned_data
