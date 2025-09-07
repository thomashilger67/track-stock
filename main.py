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
        s3_key = f"{ticker}/{today}.parquet"


        stock_data = yf.Ticker(ticker)

        stock_data_today= stock_data.history(period="1d", interval="5m")
        buffer = BytesIO()
        stock_data_today.to_parquet(buffer, compression="snappy")
        buffer.seek(0)

        s3.upload_fileobj(buffer, bucket_name, s3_key)
        print(f"Uploaded {s3_key} to bucket {bucket_name}")


if __name__== '__main__':
    main()






