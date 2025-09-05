import yfinance as yf
import requests 
import pyarrow
from datetime import date

ticker= "ONON"
today=date.today().isoformat()

stock_data = yf.Ticker(ticker)

stock_data_today= stock_data.history(period="1d", interval="5m")

stock_data_today.to_parquet(path=f"{ticker}-{today}.parquet.gzip", compression="gzip")








