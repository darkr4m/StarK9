from django.db import models
from django.utils import timezone
from django.core import validators as v
from .validators import validate_name, validate_phone_number

class Address(models.Model):
    """
    TODO: Add country field
        pip install django-countries
        django-countries.CountryField
    TODO: Add international support for phone numbers
        pip install django-phonenumber-field[phonenumbers]
        PhoneNumberField
        add 'phonenumber_field' to INSTALLED_APPS in settings.py
    """
    
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name='addresses',
        help_text="The client this address belongs to."
    )
    ADDRESS_TYPE_CHOICES = [
        ('HOME', 'Home'),
        ('WORK', 'Work'),
        ('BILLING', 'Billing'),
        ('OTHER', 'Other')
    ]
    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPE_CHOICES,
        default='HOME',
        blank=False,
        help_text="Type of address."
    )
    street_address_1 = models.CharField(
        max_length=255,
        blank=False,
        help_text="Primary street address line (e.g., '123 Main St'). Required."
    )
    street_address_2 = models.CharField(
        max_length=255, 
        blank=True,
        help_text="Secondary street address line (e.g., 'Apt 4B', 'Suite 100'). Optional.")
    city = models.CharField(
        max_length=100,
        help_text="City name. Required.")
    state_province = models.CharField(
        "State / Province / Region", 
        max_length=50, 
        blank=True,
        help_text="State, province, or region name. Optional.") # Blank if not applicable everywhere
    postal_code = models.CharField(
        "Postal / Zip Code",
        max_length=20,
        blank=False,
        help_text="Postal or ZIP code. Required.")
    
    class Meta:
        verbose_name_plural = "Addresses"
        #  Ensure one client doesn't have two 'HOME' addresses, etc.
        unique_together = [['client', 'address_type']]

    def __str__(self):
        address_parts = filter(None, [
            self.street_address_1,
            self.street_address_2,
            self.city,
            self.state_province,
            self.postal_code
        ])
        return F"{self.client} - {self.get_address_type_display()}: {', '.join(address_parts)}"

# Client Model
class Client(models.Model):
    """
    Represents a client (dog owner)
    """
    # Basic information
    first_name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text="First name of the client. Required.",
        validators=[v.MinLengthValidator(2), validate_name]
    )
    last_name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text="Last name of the client. Required.",
        validators=[v.MinLengthValidator(2), validate_name]
    )
    email = models.EmailField(
        max_length=254,         # Standard max length for emails
        unique=True,            # Ensures no two clients have the same email
        null=False,
        blank=False,
        help_text="Client's primary email address. Required."
    )
    phone_number = models.CharField(
        max_length=20,          # Allows for various phone number formats
        null=False,
        blank=False,
        help_text="Client's primary phone number. Required.",
        validators=[v.MinLengthValidator(2), validate_phone_number]
    )

    # Tracking Information
    date_added = models.DateTimeField(
        default=timezone.now,   # Sets the date when the client is added
        editable=False,         # Prevents this field from being edited later
        help_text="Date the client was added to the system."
    )
    is_active = models.BooleanField(
        default=True,           # Assumes clients are active by default
        help_text="Designates whether this client is currently active."
    )

    # Optional general notes about the client
    notes = models.TextField(
        blank=True,
        help_text="General notes about the client. Optional."
    )

    class Meta:
        ordering = ['last_name', 'first_name'] # Order clients alphabetically by last name by default
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    

