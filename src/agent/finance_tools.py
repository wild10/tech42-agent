import yfinance as yf
from langchain.tools import tool
from datetime import datetime, timedelta

@tool
def retrieve_realtime_stock_price(ticker: str):
    """
    Get the real-time stock price for a given ticker (e.g., 'AMZN') using yfinance. 
    Use this for current market valuation questions.
    """
    try:
        stock = yf.Ticker(ticker)
        # Using fast_info or basic_info for real-time data
        price = stock.info['currentPrice']
        currency = stock.info['currency']
        # price = stock.fast_info
        # currency = stock.currency
        return f"The current price of {ticker} is {price:.2f} {currency}."
    except Exception as e:
        return f"Error retrieving price for {ticker}: {str(e)}"

@tool
def retrieve_historical_stock_price(ticker: str, period: str = "1mo"):
    """
    Get historical stock prices for a given ticker (e.g., 'AMZN') and period. 
    Period options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max. 
    Use this for trend analysis and historical performance comparisons.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        if hist.empty:
            return f"No historical data found for {ticker} over the period {period}."
        
        # Format the output to be concise but informative
        last_close = hist['Close'].iloc[-1]
        start_close = hist['Close'].iloc[0]
        change = ((last_close - start_close) / start_close) * 100
        
        summary = (
            f"Historical data for {ticker} over {period}:\n"
            f"- Start price: {start_close:.2f}\n"
            f"- Current/Last close: {last_close:.2f}\n"
            f"- Percentage change: {change:+.2f}%\n"
            f"- Max price: {hist['High'].max():.2f}\n"
            f"- Min price: {hist['Low'].min():.2f}"
        )
        return summary
    except Exception as e:
        return f"Error retrieving historical data for {ticker}: {str(e)}"
