# Client Model

## Description
`Client(models.Model)`: Represents a client (dog owner) in the system. This model stores essential contact information, tracking details like when the client was added, and their active status.

## Fields

| Field         | Type          | Constraints                             | Description                                                                 | Validators                                                                     |
|---------------|---------------|-----------------------------------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| `id`          | `AutoField`   | Primary Key                             | Auto-incrementing unique identifier. (Implicit)                             | -                                                                              |
| `first_name`  | `CharField`   | `max_length=200`, Not Null, Not Blank   | **Required.** First name of the client.                                     | `MinLengthValidator(2)`, `validate_name`                                       |
| `last_name`   | `CharField`   | `max_length=200`, Not Null, Not Blank   | **Required.** Last name of the client.                                      | `MinLengthValidator(2)`, `validate_name`                                       |
| `email`       | `EmailField`  | `max_length=254`, Unique, Not Null, Not Blank | **Required.** Client's primary email. Must be unique.                     | Django's `EmailValidator` (Implicit)                                           |
| `phone_number`| `CharField`   | `max_length=20`, Not Null, Not Blank    | **Required.** Client's primary phone number.                              | `MinLengthValidator(2)`, `validate_phone_number`                               |
| `date_added`  | `DateTimeField`| Not Editable, Default `timezone.now()`  | Timestamp when created. Set automatically. Not user-required (has default). | -                                                                              |
| `is_active`   | `BooleanField`| Default `True`                          | Designates if client is active. Not user-required (has default).            | -                                                                              |
| `notes`       | `TextField`   | Blank Allowed                           | **Optional.** General notes about the client.                               | -                                                                              |

## Constraints

* **Database Level:**
    * `id`: Primary Key. Automatically managed by Django.
    * `email`: `UNIQUE` constraint. Ensures no two clients can have the same email address.
    * `first_name`, `last_name`, `email`, `phone_number`: `NOT NULL` constraint. These fields cannot be empty at the database level.
* **Validation Level:**
    * `first_name`, `last_name`, `email`, `phone_number`: `blank=False`. These fields are required in forms and the Django admin.
    * `date_added`: `editable=False`. This field cannot be modified through forms or the Django admin after initial creation.
    * `is_active`: `default=True`. New clients are active by default.
    * `notes`: `blank=True`. This field is optional and can be left empty in forms.

## Additional Validators

* **`first_name`**:
    * `MinLengthValidator(2)`: Ensures the first name has at least 2 characters.
    * `validate_name`: Custom validator. Checks that the name contains only Unicode letters (a-z, A-Z), whitespace characters, hyphens (`-`), and apostrophes (`'`). Strips leading/trailing whitespace before validation. Raises `ValidationError` with message: "Name can only contain letters, marks, spaces, hyphens, and apostrophes."
* **`last_name`**:
    * `MinLengthValidator(2)`: Ensures the last name has at least 2 characters.
    * `validate_name`: Custom validator. Same checks as for `first_name`.
* **`email`**:
    * Implicitly uses Django's built-in `EmailValidator` for standard email format validation.
* **`phone_number`**:
    * `MinLengthValidator(2)`: Ensures the phone number has at least 2 characters.
    * `validate_phone_number`: Custom validator. Checks if the phone number matches common North American formats using regex `^\+?1?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$`. This allows optional country code (+1), optional parentheses around area code, and spaces, hyphens, or dots as separators (e.g., `555-123-4567`, `(555) 123-4567`, `+1.555.123.4567`). Strips leading/trailing whitespace before validation. Raises `ValidationError` with message: "Phone number must be in XXX-XXX-XXXX format." (Note: the regex allows more formats than just the message implies).

## String Representation (`__str__`)

When a `Client` object is represented as a string (e.g., in the Django admin or shell), it displays the client's name in the format: `"LastName, FirstName"`.

*Example:* For a client with `first_name="Jane"` and `last_name="Doe"`, the string representation would be `"Doe, Jane"`.

## Meta Information

The inner `Meta` class provides metadata for the model:

* `ordering = ['last_name', 'first_name']`: Specifies that when querying multiple `Client` objects without an explicit `order_by()` clause, the results should be sorted primarily by `last_name` (ascending) and secondarily by `first_name` (ascending).
* `verbose_name = "Client"`: Sets the user-friendly singular name for the model, used in the Django admin interface (e.g., "Add Client").
* `verbose_name_plural = "Clients"`: Sets the user-friendly plural name for the model, used in the Django admin interface (e.g., "View Clients").

## JSON Structure (Example)

When serialized (e.g., through Django REST Framework or other API methods), a `Client` object typically looks like this:

```json
{
  "id": 1,
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com",
  "phone_number": "555-123-4567",
  "date_added": "2025-03-31T18:42:06.543Z", // Example ISO 8601 format (current time used for example)
  "is_active": true,
  "notes": "Prefers contact via email."
}
