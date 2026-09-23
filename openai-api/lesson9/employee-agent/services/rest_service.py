import requests
from config import FRANKFURTER_URL

class RestService:

    def get_exchange_rate(self, base_currency, quote_currency):
        url = (
            f"{FRANKFURTER_URL}/rate/"
            f"{base_currency.upper()}/"
            f"{quote_currency.upper()}"
        )

        response = requests.get(
            url,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        return {
            "success": True,
            "base_currency":
                data["base"],
            "quote_currency":
                data["quote"],
            "rate":
                data["rate"],
            "date":
                data.get("date")
        }