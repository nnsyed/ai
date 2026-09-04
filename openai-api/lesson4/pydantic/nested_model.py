from pydantic import BaseModel


class Address(BaseModel):
  city: str
  zip_code: str


class Customer(BaseModel):
  name: str
  address: Address


cust = Customer(name="Bob", address={"city": "New York", "zip_code": "10001"})
print(cust.model_dump())
