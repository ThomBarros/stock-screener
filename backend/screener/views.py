from django.shortcuts import render
from rest_framework import viewsets
from .models import Screener
from .serializers import ScreenerSerializer

# Create your views here.

class ScreenerView(viewsets.ModelViewSet):
    serializer_class = ScreenerSerializer
    queryset = Screener.objects.all()