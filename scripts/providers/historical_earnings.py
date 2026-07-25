import requests

from scripts.config import FMP_API_KEY


url = f"https://financialmodelingprep.com/api/v3/earnings-surprises/AAPL?apikey={FMP_API_KEY}"

response = requests.get(url)

print(response.status_code)
print(response.text)