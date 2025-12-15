from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Screener, Stock
from .serializers import ScreenerSerializer, StockSerializer
from .services import get_prev_close_price

# Create your views here.

class ScreenerView(viewsets.ModelViewSet):
    serializer_class = ScreenerSerializer
    queryset = Screener.objects.all()

class StockView(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    @action(detail=False, methods=["get", "post"])
    def fetch_prev_close(self, request):
        ticker = (
            request.data.get("ticker")
            if request.method == "POST"
            else request.query_params.get("ticker")
        )

        if not ticker:
            return Response(
                {"error": "ticker is required"},
                status=400
            )

        price = get_prev_close_price(ticker)
        return Response({"prev_close": price})