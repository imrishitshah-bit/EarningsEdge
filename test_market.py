import requests

from scripts.config import FMP_API_KEY

url = (
    "https://financialmodelingprep.com/stable/historical-price-eod/full"
    f"?symbol=AAPL&apikey={FMP_API_KEY}"
)

response = requests.get(url)
response.raise_for_status()

data = response.json()

print(type(data))
print(len(data))

print(data[0])