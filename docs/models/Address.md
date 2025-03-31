# Address Model

## Description

Represents a physical address associated with a `Client`. It stores standard address components: `street`, `city`, `postal code`, and `type` (e.g., Home, Work). Each address must be linked to a specific client.

*(Note: The current implementation primarily targets US-style addresses. Future enhancements include potentially adding a dedicated country field using `django-countries` and support for international phone numbers via `django-phonenumber-field`.)*

## Fields

| Field             | Type         | Constraints                                | Description                                                                    | Validators |
|-------------------|--------------|--------------------------------------------|--------------------------------------------------------------------------------|------------|
| `id`              | `AutoField`  | Primary Key                                | Auto-incrementing unique identifier. (Implicit)                                | -          |
| `client`          | `ForeignKey` | Not Null, `on_delete=CASCADE`              | **Required.** Link to the `Client` this address belongs to.                     | -          |
| `address_type`    | `CharField`  | `max_length=10`, `choices`, `default='HOME'`, Not Blank | **Required.** Type of address. Choices: 'Home', 'Work', 'Billing', 'Other'. Defaults to 'Home'. | -          |
| `street_address_1`| `CharField`  | `max_length=255`, Not Blank                | **Required.** Primary street address line (e.g., '123 Main St').              | -          |
| `street_address_2`| `CharField`  | `max_length=255`, Blank Allowed            | **Optional.** Secondary line (e.g., 'Apt 4B', 'Suite 100').                   | -          |
| `city`            | `CharField`  | `max_length=100`, Not Blank                | **Required.** City name.                                                        | -          |
| `state_province`  | `CharField`  | `max_length=50`, Blank Allowed             | **Optional.** State, province, or region. Verbose Name: "State / Province / Region". | -          |
| `postal_code`     | `CharField`  | `max_length=20`, Not Blank                 | **Required.** Postal or ZIP code. Verbose Name: "Postal / Zip Code".           | -          |

## Constraints

* **Database Level:**
    * `id`: Primary Key.
    * `client`: Foreign Key constraint linking to the `Client` model's `id`. `NOT NULL`. If a `Client` is deleted, their associated `Address` records are also deleted due to `on_delete=models.CASCADE`.
    * `unique_together = [['client', 'address_type']]`: A `UNIQUE` constraint across the combination of the `client` foreign key and the `address_type` field. This prevents a single client from having multiple addresses designated with the same type (e.g., a client can only have one 'HOME' address).
* **Validation Level:**
    * `client`, `address_type`, `street_address_1`, `city`, `postal_code`: `blank=False`. These fields are required in forms and the Django admin.
    * `street_address_2`, `state_province`: `blank=True`. These fields are optional and can be left empty in forms.
    * `address_type`: Must be one of the predefined `ADDRESS_TYPE_CHOICES` (`HOME`, `WORK`, `BILLING`, `OTHER`). It has a `default` value of `'HOME'`.

## Additional Validators

* No specific custom field validators are defined directly within this model's code.
* Standard Django field type validations apply based on the field type and constraints (e.g., `CharField` respects `max_length`, `ForeignKey` ensures the related client exists).

## String Representation (`__str__`)

When an `Address` object is represented as a string, it combines:
1.  The string representation of the associated `Client` object (e.g., "Doe, Jane").
2.  The user-friendly display name of the `address_type` (e.g., "Home").
3.  A comma-separated string of the non-empty address components: `street_address_1`, `street_address_2`, `city`, `state_province`, `postal_code`.

*Example:* For an address belonging to client "Doe, Jane", with type 'HOME', street "123 Main St", city "Anytown", state "TX", and postal code "75070", the string representation would be:
`"Doe, Jane - Home: 123 Main St, Anytown, TX, 75070"`

If `street_address_2` or `state_province` were empty, they would be omitted from the address part.

## Meta Information

The inner `Meta` class provides metadata for the model:

* `verbose_name_plural = "Addresses"`: Sets the user-friendly plural name for the model, primarily used in the Django admin interface (e.g., "View Addresses").
* `unique_together = [['client', 'address_type']]`: Enforces uniqueness for the combination of the `client` and `address_type` fields at the database level.

## JSON Structure (Example)

When serialized (e.g., via Django REST Framework), an Address object might look like this:

```json
{
  "id": 22,
  "client": 5, // Foreign Key ID referencing the Client object
  "address_type": "HOME", // Raw value stored in the database
  "get_address_type_display": "Home", // User-friendly value, often included by serializers
  "street_address_1": "456 Oak Avenue",
  "street_address_2": null, // Could be null or "" if empty
  "city": "Somewhere",
  "state_province": "CA",
  "postal_code": "90210"
}
