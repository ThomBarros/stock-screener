import yfinance as yf
from decimal import Decimal
from django.shortcuts import get_object_or_404
from .models import Stock

def get_stock_info(ticker: str):
    try:
        ticker = ticker.upper()
        stock = yf.Ticker(ticker)
        info = stock.info

        if info is not None:
            return {
                "stock_ticker": info.get("symbol"),
                "stock_name": info.get("shortName") or info.get("longName"),
                "recent_price": info.get("regularMarketPreviousClose"),
            }

    except Exception:
        return None

def get_prev_close_price(ticker: str) -> Decimal:
    ticker = ticker.upper()

    stock = get_object_or_404(Stock, stock_ticker=ticker)

    yf_ticker = yf.Ticker(ticker)

    prev_close = yf_ticker.info["regularMarketPrice"]

    stock.recent_price = prev_close
    stock.save(update_fields=["recent_price"])

    return prev_close
