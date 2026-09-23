from services.rest_service import RestService

rest = RestService()

def get_exchange_rate(base_currency, quote_currency):
    return rest.get_exchange_rate(base_currency, quote_currency)
