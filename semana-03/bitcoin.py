from dotenv import load_dotenv
import os
import requests
import sys
import json


load_dotenv()
myAPIkey = os.getenv("COINCAP_API_KEY")

try:
    if len(sys.argv) < 2:
        sys.exit("Missing command-line argument")
    amount = float(sys.argv[1])
except (ValueError, IndexError):
    sys.exit("Command-line argument is not a number")

try:
    response = requests.get(f"https://rest.coincap.io/v3/assets/bitcoin?apiKey={myAPIkey}")
except (requests.RequestException): 
    sys.exit("Command-line argument is not a number")

clean_response = response.json()
market_price = clean_response["data"]["priceUsd"]
user_price = float(market_price) * amount 

print(f"${user_price:,.4f}")