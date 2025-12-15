import yfinance as yf
from decimal import Decimal

def scrape_stock_info(ticker):
    stock = yf.Ticker(ticker)
    stock_info = stock.info
    return stock_info

def get_prev_close_price(ticker):
    yf_ticker = yf.Ticker(ticker)

    prev_close = yf_ticker.info["regularMarketPrice"]
    return prev_close

if __name__=="__main__":
    dat = get_prev_close_price("MSFT")
    print(dat)