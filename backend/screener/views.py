from django.shortcuts import render
from rest_framework import viewsets
from .models import Screener, Stock
from .serializers import ScreenerSerializer, StockSerializer

# Create your views here.

class ScreenerView(viewsets.ModelViewSet):
    serializer_class = ScreenerSerializer
    queryset = Screener.objects.all()

class StockView(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()