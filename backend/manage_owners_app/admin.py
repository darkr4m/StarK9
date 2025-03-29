from django.contrib import admin
from .models import Client

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'phone_number', 'is_active')
    list_filter = ['is_active']
    search_fields = ('last_name', 'email', 'phone_number')