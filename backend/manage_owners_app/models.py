from django.db import models
from django.utils import timezone
from django.core import validators as v
from .validators import validate_name, validate_phone_number

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
    address = models.TextField(
        blank=True,
        help_text="Client's physical address (optional)."
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
        help_text="General notes about the client (optional)."
    )

    class Meta:
        ordering = ['last_name', 'first_name'] # Order clients alphabetically by last name by default
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"