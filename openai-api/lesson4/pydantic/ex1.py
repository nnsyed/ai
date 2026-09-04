from pydantic import BaseModel

class User(BaseModel):
  id: int
  name: str
  email: str | None = None


user = User(id=1, name="Alice", email="alice@example.com")
print(user.model_dump())
