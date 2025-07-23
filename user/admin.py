from django.contrib import admin
from .models import UserDetails

# Register the models you have created here
@admin.register(UserDetails)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'is_active', 'is_staff')
    search_fields = ('email', 'name')
