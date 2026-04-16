from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TopUpRequest

admin.site.register(CustomUser, UserAdmin)

@admin.register(TopUpRequest)
class TopUpRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username',)

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = TopUpRequest.objects.get(pk=obj.pk)
            # If changing from pending to approved, add balance
            if old_obj.status == 'pending' and obj.status == 'approved':
                user = obj.user
                user.balance += obj.amount
                user.save()
        super().save_model(request, obj, form, change)
