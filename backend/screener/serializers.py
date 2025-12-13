from rest_framework import serializers
from .models import Screener, Stock

class ScreenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screener
        fields = ('id', 'title', 'description', 'completed')

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'stock_ticker', 'stock_name', 'recent_price')