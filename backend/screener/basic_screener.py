import yfinance as yf
from typing import Dict, List
import requests

SEC_TICKER_CIK_URL = "https://www.sec.gov/files/company_tickers.json"
HEADERS = {
    "User-Agent": "User Name username@example.com"
}

# def get_ticker_list(stock_list: List) -> Dict:
#     ticker_list = {}
#     for ticker in stock_list:
#         try:
#             ticker = ticker.upper()
#             stock = yf.Ticker(ticker)
#             ticker_list[ticker] = stock
#         except Exception:
#             return None
    
#     return ticker_list

def get_ticker_list(stock_list: List):
    stocks = ' '.join(stock_list)
    tickers = yf.Tickers(stocks)
    return tickers


def get_fast_info_tickers(tickers):
    info = {}
    try:
        for symbol, ticker in tickers.tickers.items():
            fast_info = ticker.fast_info
            info[symbol] = fast_info
    except Exception:
        pass

    return info

def market_cap_screen(tickers, min, max):
    market_caps = {}
    for symbol, ticker in tickers.tickers.items():
        try:
            stock_market_cap = float(ticker.fast_info.market_cap)
        except Exception:
            continue
        
        if min == None and max == None:
            market_caps[symbol] = stock_market_cap
        elif min == None and max != None:
            if stock_market_cap < max:
                market_caps[symbol] = stock_market_cap
            else:
                continue
        elif max == None and min != None:
            if stock_market_cap > min:
                market_caps[symbol] = stock_market_cap
            else:
                continue
        else:
            if stock_market_cap > min and stock_market_cap < max:
                market_caps[symbol] = stock_market_cap
            else:
                continue

    return market_caps



def ev_to_ebitda_screen(tickers, min, max):
    ev_to_ebitdas = {}
    for symbol, ticker in tickers.tickers.items():
        ev_to_ebitda = ticker.info.enterpriseToEbitda
        if ev_to_ebitda == None:
            continue
        elif ev_to_ebitda < min:
            continue
        elif ev_to_ebitda > max:
            continue
        else:
            ev_to_ebitdas[symbol] = ev_to_ebitda

    return ev_to_ebitdas


def get_sec_stocks():
    stocks = []
    resp = requests.get(SEC_TICKER_CIK_URL, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    for company in data.values():
        stocks.append(company["ticker"])
    return stocks





if __name__=="__main__":
    stocks = get_sec_stocks()
    tickers = get_ticker_list(stocks)
    #info = get_fast_info_tickers(tickers)
    market_caps = market_cap_screen(min=938643789356, max=None, tickers=tickers)