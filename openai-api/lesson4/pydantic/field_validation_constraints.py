from pydantic import BaseModel, Field


class Product(BaseModel):
  name: str = Field(min_length=2, max_length=50)
  price: float = Field(gt=0)
  in_stock: bool = True


item = Product(name="Laptop", price=999.99)
print(item.model_dump())
