from django.shortcuts import render
from rest_framework import viewsets
from .models import Player
from .serializers import PlayerSerializers


# Create your views here.
class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializers
