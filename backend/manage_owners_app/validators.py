from django.core.exceptions import ValidationError

import re

def validate_name(name):
    """
    Validates a name allowing Unicode letters, spaces, hyphens, and apostrophes.
    """
    error_message = "Name can only contain letters, marks, spaces, hyphens, and apostrophes."
    regex = r"^[a-zA-Z\s'-]+$"
    name = name.strip()
    good_name = re.match(regex, name)
    if good_name:
        return name
    else:
        raise ValidationError(error_message, params= { "name" : name })
    
def validate_phone_number(phone_number):
    error_message = "Phone number must be in XXX-XXX-XXXX format."
    regex = r'^\+?1?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$'
    phone_number =phone_number.strip()
    good_phone_number = re.match(regex, phone_number)
    if good_phone_number:
        return phone_number
    else:
        raise ValidationError(error_message, params= { "phone_number" : phone_number })