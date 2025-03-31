from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Client, Address
# from .validators import validate_name,validate_phone_number

# Create your tests here.
class ClientModelTests(TestCase):

    def setUp(self):
        """Set up non-modified objects used by all test methods."""
        self.client_data = {
            'first_name': 'John',
            'last_name' : 'Doe',
            'email' : 'john.doe@example.com',
            'phone_number' : '678-640-8681'
        }
    
    def test_01_client_creation_successful(self):
        """Test creating a Client instance successfully."""
        client = Client.objects.create(**self.client_data)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(client.first_name, 'John')
        self.assertEqual(client.last_name, 'Doe')
        self.assertEqual(client.email, 'john.doe@example.com' )
        self.assertEqual(client.phone_number, '678-640-8681')
        self.assertTrue(client.is_active)
        self.assertIsNotNone(client.date_added)

    def test_02_client_string_representation(self):
        """Test the __str__ method."""
        client = Client.objects.create(**self.client_data)
        self.assertEqual(str(client), "Doe, John")

    def test_03_client_required_fields(self):
        """Test that required fields raise ValidationError on full_clean."""
        required_fields = ['first_name', 'last_name', 'email', 'phone_number']
        for field in required_fields:
            data = self.client_data.copy()
            data.pop(field) # Remove one required field
            client = Client(**data)
            with self.assertRaises(ValidationError, msg=f"Field '{field}' should be required"):
                # Use full_clean() to trigger model validation before saving
                client.full_clean()
        
        for field in required_fields:
            data = self.client_data.copy()
            data[field] = "" #set to blank
            client = Client(**data)
            with self.assertRaises(ValidationError, msg=f"Field '{field}' should not allow blank"):
                client.full_clean()

    def test_04_client_unique_email(self):
        """Test that the email field must be unique."""
        Client.objects.create(**self.client_data) # Create the first client
        dupe_data = self.client_data.copy()
        dupe_data['first_name'] = 'Jane'
        dupe_data['phone_number'] = '369-450-0024'
        client_dupe = Client(**dupe_data)
        with self.assertRaises(ValidationError, msg="full_clean() should raise ValidationError for duplicate email"):
            client_dupe.full_clean()

    def test_05_client_name_validators(self):
        """Test custom and built-in validators."""
        invalid_names = ["X", "Dee1", "Yoe!"]
        for name in invalid_names:
            with self.subTest(name=name): # Subtests for better error reporting
                data = self.client_data.copy()
                data['first_name'] = name
                client = Client(**data)
                with self.assertRaises(ValidationError, msg="full_clean() should raise ValidationError for invalid names"):
                    client.full_clean() # Should fail validation

    def test_06_client_phone_number_validation(self):
        """Test custom phone number validator."""
        invalid_phone_numbers = ["invalid","666-4353","222 222 222"]
        for number in invalid_phone_numbers:
            with self.subTest(name=number): # Subtests for better error reporting
                data = self.client_data.copy()
                data['phone_number'] = number
                client = Client(**data)
                with self.assertRaises(ValidationError, msg="full_clean() should raise ValidationError for invalid phone number format"):
                    client.full_clean() # Should fail phone validation

    def test_07_client_email_validation(self):
        """Test built-in EmailField validation."""
        invalid_email = "not-an-email"
        data = self.client_data.copy()
        data['email'] = invalid_email
        client = Client(**data)
        with self.assertRaises(ValidationError, msg="full_clean() should raise ValidationError for invalid email"):
            client.full_clean() # Should fail email validation

    def test_08_client_defaults(self):
        client = Client.objects.create(**self.client_data)
        self.assertTrue(client.is_active)
        self.assertTrue(isinstance(client.date_added, timezone.datetime))
        # Check if date_added is recent (within a reasonable tolerance)
        self.assertTrue(timezone.now() - client.date_added < timezone.timedelta(seconds=5))

    def test_09_client_ordering(self):
        """Test the default ordering specified in Meta."""
        Client.objects.create(first_name = 'Charles', last_name = 'Browne', email = 'c.brown@yodel.com', phone_number = '134-321-4567')
        Client.objects.create(first_name = 'Alice', last_name = 'Smith', email = 'a.smith@yodel.com', phone_number = '134-321-4569')
        Client.objects.create(first_name = 'Bob', last_name = 'Smith', email = 'b.smith@yodel.com', phone_number = '134-321-4269')

        clients = list(Client.objects.all()) # Get ordered list

        self.assertEqual(clients[0].last_name, "Browne")
        self.assertEqual(clients[1].last_name, "Smith")
        self.assertEqual(clients[1].first_name, "Alice") # Alice Smith before Bob Smith
        self.assertEqual(clients[2].last_name, "Smith")
        self.assertEqual(clients[2].first_name, "Bob")


class AddressModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole class. Creates a client once.
        Using setUpTestData for data needed across multiple tests that isn't modified.
        """
        cls.client_data = Client.objects.create(
            first_name = 'Test',
            last_name = 'Client',
            email = 'test.client@ex.com',
            phone_number = '987-234-5678'
        )
    def setUp(self):
        """Set up data needed for each individual test."""
        self.address_data = {
            'client' : self.client_data,
            'address_type' : 'HOME',
            'street_address_1' : '123 Easy Street',
            'city' : 'Atown',
            'postal_code' : '34567',
            # Optional fields initially blank
            'street_address_2' : '',
            'state_province' : ''
        }

    def test_01_address_creation_successful(self):
        """Test creating an Address instance successfully."""
        address = Address.objects.create(**self.address_data)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(address.client, self.client_data)
        self.assertEqual(address.address_type, 'HOME')
        self.assertEqual(address.street_address_1, '123 Easy Street')
        self.assertEqual(address.city, 'Atown')
        self.assertEqual(address.postal_code, '34567')
        self.assertEqual(address.street_address_2, '') # Check optional field
        self.assertEqual(address.state_province, '') # Check optional field

    def test_02_address_creation_with_optional_fields(self):
        """Test creating an Address with optional fields populated."""
        data = self.address_data.copy()
        data['street_address_2'] = 'Apt 6T'
        data['state_province'] = 'TX'
        address = Address.objects.create(**data)
        self.assertEqual(address.street_address_2, 'Apt 6T')
        self.assertEqual(address.state_province, 'TX')
    
    def test_03_address_str_rep(self):
        """Test the __str__ method with and without optional fields."""
        # Without optional fields
        addr1 = Address.objects.create(**self.address_data)
        expected_str1 = F"{(self.client_data)} - Home: 123 Easy Street, Atown, 34567"
        self.assertEqual(str(addr1), expected_str1)

        # With optional fields
        data = self.address_data.copy()
        data['address_type'] = 'WORK'
        data['street_address_1'] = '456 Doing A Business'
        data['street_address_2'] = 'Suite 100'
        data['city'] = 'Workworkton'
        data['state_province'] = 'NO'
        data['postal_code'] = '67890'
        addr2 = Address.objects.create(**data)
        expected_str2 = F"{self.client_data} - Work: 456 Doing A Business, Suite 100, Workworkton, NO, 67890"
        self.assertEqual(str(addr2), expected_str2)
    
    def test_04_address_required_fields(self):
        """Test that required fields raise ValidationError on full_clean."""
        # Note: 'client' is required by ForeignKey, handled differently than CharField etc.
        # 'address_type' has a default.

        required_fields = ['street_address_1','city','postal_code']

        for field in required_fields:
            data = self.address_data.copy()
            data.pop(field) # Remove required field
            address = Address(**data)
            with self.assertRaises(ValidationError, msg=f"Field '{field}' should be required"):
                address.full_clean()

        # Test blank values
        for field in required_fields:
            data = self.address_data.copy()
            data[field] = ""
            address = Address(**data)
            with self.assertRaises(ValidationError, msg=f"Field '{field}' should not allow blank"):
                address.full_clean()
    
    def test_05_address_foreign_key(self):
        """Test the ForeignKey relationship to Client."""
        address = Address.objects.create(**self.address_data)
        self.assertEqual(address.client, self.client_data)
        # Test the reverse relationship defined by related_name='addresses'
        self.assertIn(address, self.client_data.addresses.all())
        self.assertEqual(self.client_data.addresses.count(), 1)

    def test_06_address_related_name(self):
        """ Test accessing addresses from the client instance """
        addr1 = Address.objects.create(client = self.client_data, address_type = 'HOME', street_address_1='1 Home St', city='Hometown', postal_code='11122')
        addr2 = Address.objects.create(client = self.client_data, address_type='WORK', street_address_1='2 Work St', city='Worktown', postal_code='22211')

        client_addresses = self.client_data.addresses.all().order_by('address_type') # Order for consistent testing
        self.assertEqual(client_addresses.count(),2)
        self.assertIn(addr1, client_addresses)
        self.assertIn(addr2, client_addresses)
        self.assertEqual(list(client_addresses), [addr1,addr2]) # Check order HOME then WORK

    def test_07_address_default_type(self):
        """Test that address_type defaults to 'HOME'."""
        data = self.address_data.copy()
        data.pop('address_type') # Remove address_type to test default
        address = Address(**data)
        self.assertEqual(address.address_type, 'HOME')

    def test_08_address_choices_validation(self):
        """Test that invalid address_type choice raises ValidationError."""
        data = self.address_data.copy()
        data['address_type'] = 'INVALID_TYPE'
        address = Address(**data)
        with self.assertRaises(ValidationError, msg=f"full_clean() should raise ValidationError for invalid address_type choice"):
            address.full_clean()

    def test_09_address_unique_together_constraint(self):
        """Test the unique_together constraint for client and address_type."""
        # Create the first HOME address 
        Address.objects.create(**self.address_data)
        self.assertEqual(self.client_data.addresses.count(), 1)

        # Try to create another HOME address for the SAME client
        dupe_data = self.address_data.copy()
        dupe_data['street_address_1'] = "999 I am different" # Different address details
        dupe_data['address_type'] = "HOME"
        
        dupe_addr_obj = Address(**dupe_data)
        with self.assertRaises(ValidationError, msg=f"full_clean() should catch unique_together violation"):
            dupe_addr_obj.full_clean()
        
        # Verify it's still 1 address
        self.assertEqual(self.client_data.addresses.count(), 1)

        # Verify creating a DIFFERENT type ('WORK') for the SAME client works
        work_data = self.address_data.copy()
        work_data['address_type'] = "WORK"
        work_data['street_address_1'] = "3435 Working Ave"
        Address.objects.create(**work_data)
        self.assertEqual(self.client_data.addresses.count(), 2) # Should now have HOME and WORK

        # Verify creating the SAME type ('HOME') for a DIFFERENT client works
        other_client = Client.objects.create(
            first_name = "Other", last_name = "Dude", email = "dude@bro.com", phone_number = "333-222-1242"
        )
        other_client_addr = self.address_data.copy()
        other_client_addr['client'] = other_client
        other_client_addr['address_type'] = "HOME"
        Address.objects.create(**other_client_addr)
        self.assertEqual(other_client.addresses.count(), 1) # Other client has 1 address
        self.assertEqual(self.client_data.addresses.count(), 2) # Original client still has 2