from rest_client import get_exchange_rate
result = get_exchange_rate(
    "USD",
    "EUR"
)
print(result)
