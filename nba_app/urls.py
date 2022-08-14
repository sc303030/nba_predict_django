from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from .views import PlayerViewSet

router = routers.DefaultRouter()
router.register(r'players', PlayerViewSet, basename='players')

urlpatterns = [
    path('', include(router.urls))
]
