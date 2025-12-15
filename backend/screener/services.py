import yfinance as yf
from decimal import Decimal
from django.shortcuts import get_object_or_404
from .models import Stock

def get_prev_close_price(ticker: str) -> Decimal:
    ticker = ticker.upper()

    stock = get_object_or_404(Stock, stock_ticker=ticker)

    yf_ticker = yf.Ticker(ticker)

    prev_close = yf_ticker.info["regularMarketPrice"]

    stock.recent_price = prev_close
    stock.save(update_fields=["recent_price"])

    return prev_close
