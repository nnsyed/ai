from pydantic import BaseModel, field_validator


class Registration(BaseModel):
  username: str
  age: int

  @field_validator("age")
  @classmethod
  def check_age(cls, v: int) -> int:
    if v < 18:
      raise ValueError("Must be at least 18 years old")
    return v


reg = Registration(username="coder123", age=20)
print(reg.model_dump())
