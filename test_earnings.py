import requests

url = "https://financialmodelingprep.com/stable/earnings?symbol=AMD&apikey=MJyoYdUyd7hYBZo81PrEIJqPglyp125G"

data = requests.get(url).json()

print(data[0])