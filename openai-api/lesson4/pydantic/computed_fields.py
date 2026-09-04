from pydantic import BaseModel, computed_field


class Rectangle(BaseModel):
  width: float
  height: float

  @computed_field
  @property
  def area(self) -> float:
    return self.width * self.height


rect = Rectangle(width=4.0, height=5.0)
print(rect.model_dump())
