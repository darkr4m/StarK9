from django.urls import path
from .views import All_clients

urlpatterns = [
    path('', All_clients.as_view(), name='all_clients')
]