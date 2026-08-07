import csv
import io
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

ticker = "SHOP"

url = "https://www.alphavantage.co/query"

params = {
    "function": "EARNINGS_ESTIMATES",
    "symbol": ticker,
    "apikey": API_KEY,
}

response = requests.get(
    url,
    params=params,
    timeout=30,
)

print("STATUS:", response.status_code)
print(response.text)