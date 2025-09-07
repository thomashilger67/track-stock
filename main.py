import yfinance as yf
import requests 
import pyarrow
from datetime import date
from io import BytesIO
import boto3
import argparse 

parser = argparse.ArgumentParser(
                    prog='track-stock',
                    description='the ticker to download'
                    )

parser.add_argument("tickers",type=str, nargs='+', help="the tickers to download")



def main(): 
    bucket_name = "track-stock"
    args = parser.parse_args()
    tickers = [ticker.upper() for ticker in args.tickers]

    s3 = boto3.client('s3')


    today=date.today().strftime("%Y/%m/%d")
    for ticker in tickers:
        s3_key = f"{ticker}/{today}.json.gz"


        stock_data = yf.Ticker(ticker)

        stock_data_today= stock_data.history(period="1d", interval="5m")
        #stock_data_today.index = stock_data_today.index.floor("S")
        stock_data_today= stock_data_today.reset_index()
        stock_data_today["Datetime"]=stock_data_today["Datetime"].dt.floor("min")
        print(stock_data_today)
        buffer = BytesIO()
        stock_data_today.to_json(buffer, orient="records", lines=True, date_format="iso", compression="gzip")
        buffer.seek(0)

        s3.upload_fileobj(buffer, bucket_name, s3_key)
        print(f"Uploaded {s3_key} to bucket {bucket_name}")


if __name__== '__main__':
    main()
