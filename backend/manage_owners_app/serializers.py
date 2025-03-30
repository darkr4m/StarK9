from rest_framework import serializers
from .models import Client, Address

class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for the Address model
    """
    client = serializers.StringRelatedField(read_only = True)
    address_type_display = serializers.CharField(source='get_address_type_display', read_only=True)
    class Meta:
        model = Address
        fields = [
            'id',
            'client',
            'address_type',
            'address_type_display',
            'street_address_1',
            'street_address_2',
            'city',
            'state_province',
            'postal_code'
        ]
        # Make client field read-only - addresses are always managed via the client endpoint
        read_only_fields = ['client']

class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Client model, including nested addresses.
    """
    addresses = AddressSerializer(many = True)
    date_added = serializers.DateTimeField(read_only=True) # make date_added read-only explicitly

    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'addresses',
            'is_active',
            'notes',
            'date_added'
        ]
        # # Make the original foreign key field write_only to accept
        # # a client ID when creating/updating addresses via this serializer
        # extra_kwargs = {
        #     'client': {'write_only': True}
        # }