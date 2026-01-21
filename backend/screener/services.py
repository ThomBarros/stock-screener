import yfinance as yf
from decimal import Decimal
from django.shortcuts import get_object_or_404
from .models import Stock
from sec_api import QueryApi
from datetime import datetime, date
from .tasks import get_sec_financials, get_sec_primary_financials
import pandas as pd
import numpy as np
import json


def get_financials(ticker: str, consolidated: bool):
    if consolidated:
        statements = get_sec_primary_financials(ticker)
    else:
        statements = get_sec_financials(ticker)
    
    statements_json = {
        name: df.to_dict(orient="records")
        for name, df in statements.items()
    }
    return statements_json


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

def get_live_price(ticker: str) -> Decimal:
    ticker = ticker.upper()
    stock = get_object_or_404(Stock, stock_ticker=ticker)
    yf_ticker = yf.Ticker(ticker)
    live_price = yf_ticker.fast_info["last_price"]
    stock.recent_price = live_price
    stock.save(update_fields=["recent_price"])

    return Decimal(str(live_price))

def get_tearsheet_info(ticker: str):
    info = create_tearsheet_info_dict(ticker)
    info_dict = json.loads(json.dumps(info, default=custom_converter))
    return info_dict

def create_tearsheet_info_dict(ticker: str):
    ticker = ticker.upper()
    stock = get_object_or_404(Stock, stock_ticker=ticker)
    yf_ticker = yf.Ticker(ticker)
    info = yf_ticker.info
    name = info.get("shortName") or info.get("longName")
    desc = info.get("longBusinessSummary")
    market_cap = info.get("marketCap")
    exchange = info.get("exchange")
    website = info.get("website")
    return {
        "name": name,
        "description": desc,
        "market_cap": market_cap,
        "exchange": exchange,
        "website": website
    }

def custom_converter(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()   # convert dates to string
    elif isinstance(obj, (np.integer, int)):
        return int(obj)
    elif isinstance(obj, (np.floating, float, Decimal)):
        return float(obj)
    elif obj is None:
        return None
    else:
        return str(obj)