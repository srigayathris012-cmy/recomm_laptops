import requests

API_KEY = "PASTE_YOUR_RAINFOREST_API_KEY_HERE"

def get_amazon_price(asin):
    url = "https://api.rainforestapi.com/request"
    params = {
        "api_key": API_KEY,
        "type": "product",
        "amazon_domain": "amazon.in",
        "asin": asin
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        price = data["product"]["buybox_winner"]["price"]["value"]
        currency = data["product"]["buybox_winner"]["price"]["currency"]
        return f"{currency} {price}"
    except:
        return "Price unavailable"
