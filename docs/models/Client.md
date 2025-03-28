# Client Model
`Client(models.Model)`: Represents a client or dog owner
## Fields
### Name
`name` (`CharField`): A standard text field for the client's name.\
`max_length=200` * - reasonable limit for names.\
**Required by default.**
### Email
`email` (`EmailField`): Specifically designed for email addresses, providing basic format validation.
`max_length=254`
`unique=True` is important here. It prevents user from accidentally creating duplicate clients with the same email address and ensures the email can potentially be used as a unique identifier later.
**Required by default.**
### Phone Number
`phone_number` (`CharField`): Using CharField instead of a more specific number field allows flexibility for different formats (e.g., `(555) 123-4567`, `+1-555-123-4567`).\
`max_length=20` - should accommodate most formats.\
`blank=True` this field is not required when filling out forms (including the Django admin). It will be stored as an empty string ("") in the database if left blank.
### Address
`address` (`TextField`): A TextField allows for multi-line input, suitable for a full address.\
`blank=True` makes it optional.
### Date Added / Created on
`date_added` (`DateTimeField`): Records when the client record was created.\
`default=timezone.now` automatically sets the field to the current date and time when the model instance is created if no value is provided.\
`editable=False` prevents users from changing this value through forms or the admin interface after creation.\
### Active Status
`is_active` (`BooleanField`): filtering out clients you no longer work with without deleting their records (which might contain valuable historical data). Simple true/false flag.\
`default=True` makes new clients active by default.
### Notes
`notes` (`TextField`): A general-purpose field for any other relevant information about the client.\
`blank=True` makes it optional.
