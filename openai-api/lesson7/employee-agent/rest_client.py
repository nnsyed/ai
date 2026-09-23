import requests
FRANKFURTER_URL=("https://api.frankfurter.dev/v2")
def get_exchange_rate(base_currency,quote_currency):
    url = ( f"{FRANKFURTER_URL}/rate/" f"{base_currency.upper()}/" f"{quote_currency.upper()}" )
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "base_currency": data["base"],
            "quote_currency": data["quote"],
            "rate": data["rate"],
            "date":data.get("date")
        }
    except requests.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }

def convert_currency(amount,exchange_rate):
    converted_amount = (amount * exchange_rate)
    return {
        "original_amount":round(amount, 2),
        "exchange_rate": exchange_rate,
        "converted_amount":round(converted_amount, 2)
    }
