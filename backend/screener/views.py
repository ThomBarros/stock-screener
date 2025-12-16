from django.shortcuts import render
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Screener, Stock
from .serializers import ScreenerSerializer, StockSerializer
from .services import get_prev_close_price, get_stock_info


# Create your views here.

class ScreenerView(viewsets.ModelViewSet):
    serializer_class = ScreenerSerializer
    queryset = Screener.objects.all()

class StockView(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    @action(detail=False, methods=["get"])
    def search_for_stock(self, request):
        ticker = request.query_params.get("ticker").upper().strip()

        if not ticker:
            return Response(
                {"error": "ticker is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        stock_data = get_stock_info(ticker)
        if not stock_data:
            return Response(
                {"error": "Stock not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            stock = Stock.objects.create(**stock_data)
            return Response(
                StockSerializer(stock).data,
                status=status.HTTP_201_CREATED
            )

        except IntegrityError:
            stock = Stock.objects.get(stock_ticker=ticker)
            return Response(
                StockSerializer(stock).data,
                status=status.HTTP_200_OK
            )


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