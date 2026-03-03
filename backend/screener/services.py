import yfinance as yf
from decimal import Decimal
from django.shortcuts import get_object_or_404
from .models import Stock
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
    sector = info.get("sector")
    phone = info.get("phone")
    industry = info.get("industry")
    currency = info.get("currency")
    employees = info.get("fullTimeEmployees")
    country = info.get("country")
    enterprise_value = info.get("enterpriseValue")
    dividend_rate = info.get("dividendRate")
    dividend_yield = info.get("dividendYield")
    payout_ratio = info.get("payoutRatio")
    beta = info.get("beta")
    volume = info.get("volume")
    trailing_PE = info.get("trailingPE")
    forward_PE = info.get("forwardPE")
    regular_market_volume = info.get("regularmarketVolume")
    shares_outstanding = info.get("sharesOutstanding")
    implied_shared_outstanding = info.get("impliedSharedOutstanding")
    book_value = info.get("bookValue")
    price_to_book = info.get("priceToBook")
    net_income_to_common = info.get("netIncomeToCommon")
    trailing_eps = info.get("trailingEps")
    forward_eps = info.get("forwardEps")
    enterprise_to_revenue = info.get("enterpriseToRevenue")
    enterprise_to_ebitda = info.get("enterpriseToEbita")
    total_cash = info.get("totalCash")
    total_cash_per_share = info.get("totalCashPerShare")
    ebitda = info.get("ebitda")
    total_debt = info.get("totalDebt")
    quick_ratio = info.get("quickRatio")
    current_ratio = info.get("currentRatio")
    total_revenue = info.get("totalRevenue")
    debt_to_equity = info.get("debtToEquity")
    revenue_per_share = info.get("revenuePerShare")
    return_on_assets = info.get("returnOnAssets")
    return_on_equity = info.get("returnOnEquity")
    return_on_equity = info.get("returnOnEquity")
    gross_profits = info.get("grossProfits")
    free_cash_flow = info.get("freeCashFlow")
    operating_cash_flow = info.get("operatingCashFlow")
    earnings_growth = info.get("earningsGrowth")
    revenue_growth = info.get("revenueGrowth")
    gross_margins = info.get("grossMargins")
    ebitda_margins = info.get("ebitdaMargins")
    operating_margins = info.get("operatingMargins")
    corporate_actions= info.get("corporateActions")
    full_exchange_name = info.get("fullExchangeName")
    eps_trailing_twelve_months = info.get("epsTrailingTwelveMonths")
    eps_forward= info.get("epsForward")
    eps_current_year = info.get("epsCurrentYear")
    price_eps_current_year = info.get("priceEpsCurrentYear")
     
    return {
        "name": name,
        "description": desc,
        "market_cap": market_cap,
        "exchange": exchange,
        "website": website,
        "sector": sector,
        "phone": phone,
        "industry": industry,
        "currency": currency,
        "employees": employees,
        "country": country,
        "enterprise_value": enterprise_value, 
        "dividend_Rate": dividend_rate, 
        "dividend_Yield" : dividend_yield, 
        "payout_Ratio" : payout_ratio, 
        "beta": beta,
        "trailing_PE": trailing_PE,
        "forward_PE": forward_PE, 
        "volume": volume, 
        "regular_Market_Volume": regular_market_volume, 
        "shares_Outstanding":shares_outstanding, 
        "implied_Shares_Outstanding": implied_shared_outstanding, 
        "book_Value": book_value, 
        "price_To_Book": price_to_book, 
        "net_Income_To_Common": net_income_to_common, 
        "trailing_Eps": trailing_eps, 
        "forward_Eps": forward_eps, 
        "enterprise_To_Revenue": enterprise_to_revenue, 
        "enterprise_To_Ebitda": enterprise_to_revenue, 
        "total_Cash": total_cash, 
        "total_Cash_Per_Share": total_cash_per_share, 
        "ebitda": ebitda, 
        "total_Debt": total_debt, 
        "quick_Ratio": quick_ratio, 
        "current_Ratio": current_ratio, 
        "total_Revenue": total_revenue, 
        "debt_To_Equity": debt_to_equity, 
        "revenue_Per_Share": revenue_per_share, 
        "return_On_Assets": return_on_assets, 
        "return_On_Equity": return_on_equity, 
        "gross_Profits": gross_profits, 
        "free_Cash_flow": free_cash_flow, 
        "operating_Cash_flow": operating_cash_flow, 
        "earnings_Growth": earnings_growth, 
        "revenue_Growth": revenue_growth, 
        "gross_Margins": gross_margins, 
        "ebitda_Margins": ebitda_margins, 
        "operating_Margins": operating_margins, 
        "corporate_Actions": corporate_actions, 
        "full_Exchange_Name": full_exchange_name, 
        "eps_Trailing_Twelve_Months": eps_trailing_twelve_months, 
        "eps_Forward": eps_forward, 
        "eps_Current_Year": eps_current_year, 
        "price_Eps_Current_Year": price_eps_current_year
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
