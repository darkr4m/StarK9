from django.contrib import admin
from .models import Client, Address


class AddressInline(admin.StackedInline):
    model = Address
    fields = ('address_type', 'street_address_1', 'street_address_2', 'city', 'state_province', 'postal_code')
    extra = 1 # # Number of empty extra forms to display by default for adding new addresses
    verbose_name = "Address"
    verbose_name_plural = "Addresses" # Verbose names specifically for the inline context
    ordering = ['address_type'] # Define ordering if needed within the inline list

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # --- List View Customization (Client list page) ---
    list_display = ('last_name', 'first_name', 'email', 'phone_number', 'is_active')
    list_filter = ['is_active']
    search_fields = ('last_name', 'email', 'phone_number')  # Enable searching across these fields
    ordering = ('last_name', 'first_name') # Default sorting 
    # --- Change/Add Form Customization (Client detail page) ---
    inlines = [AddressInline] 
    fieldsets = (
        # Section 1: Basic Info
        ('Basic Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        # Section 2: Status & Notes
        ('Status and Notes', {
            'fields' : ('notes', 'is_active'),
            'classes': ('collapse',) # Makes the section collapsible
        })
    )
    readonly_fields = ['date_added']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('client', 'address_type','city','state_province','postal_code')
    search_fields = ('street_address_1','client__last_name', 'client__email')
    autocomplete_fields = ['client']