from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Client, Address
from .serializers import ClientSerializer, AddressSerializer


class All_clients(APIView):
    """
    View to list all clients, following the basic APIView pattern.
    Handles GET requests to return a list of all clients.
    """
    def get(self, request):
        """
        Return a list of all clients.
        """
        clients = Client.objects.prefetch_related('addresses').order_by('last_name', 'first_name')
        serializer = ClientSerializer(clients, many = True)
        return Response(serializer.data)