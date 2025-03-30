from django.db import models
from django.utils import timezone
from django.core import validators as v
from .validators import validate_name, validate_phone_number

class Address(models.Model):
    
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
        help_text="Type of address."
    )
    street_address_1 = models.CharField(max_length=255)
    street_address_2 = models.CharField(
        max_length=255, 
        blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(
        "State / Province / Region", 
        max_length=20, 
        blank=True) # Blank if not applicable everywhere
    postal_code = models.CharField(
        "Postal / Zip Code",
        max_length=20)
    
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
        help_text="First name of the client.",
        validators=[v.MinLengthValidator(2), validate_name]
    )
    last_name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text="Last name of the client.",
        validators=[v.MinLengthValidator(2), validate_name]
    )
    email = models.EmailField(
        max_length=254,         # Standard max length for emails
        unique=True,            # Ensures no two clients have the same email
        null=False,
        blank=False,
        help_text="Client's primary email address."
    )
    phone_number = models.CharField(
        max_length=20,          # Allows for various phone number formats
        null=False,
        blank=False,
        help_text="Client's primary phone number.",
        validators=[v.MinLengthValidator(2), validate_phone_number]
    )

    # Address Information (Optional)
    # address = models.TextField(
    #     blank=True,
    #     help_text="Client's physical address (optional)."
    # )

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
        help_text="General notes about the client (optional)."
    )

    class Meta:
        ordering = ['last_name', 'first_name'] # Order clients alphabetically by last name by default
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    

