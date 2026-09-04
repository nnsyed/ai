from pydantic import BaseModel, ValidationError

# 1. Define your custom class by extending BaseModel
class Book(BaseModel):
    """
    A simple model representing a book.
    Pydantic automatically generates the __init__, __repr__, 
    and type validation methods behind the scenes.
    """
    title: str          # Required field: must be a string
    author: str         # Required field: must be a string
    pages: int          # Required field: must be an integer (or convertible to int)
    is_available: bool = True  # Optional field with a default value


# 2. Creating a valid instance
# Pydantic will automatically coerce compatible types (e.g., the string "328" becomes the int 328)
my_book = Book(
    title="The Hobbit",
    author="J.R.R. Tolkien",
    pages="328"  # String will be coerced into an integer
)

print("--- Valid Book Instance ---")
print(my_book)
print(f"Title: {my_book.title}")
print(f"Pages type: {type(my_book.pages)}")  # Output: <class 'int'>
print(f"Default availability: {my_book.is_available}")


# 3. Exporting to a standard Python dictionary or JSON string
print("\n--- Serializing ---")
print("Dictionary:", my_book.model_dump())
print("JSON string:", my_book.model_dump_json())


# 4. What happens when invalid data is provided?
print("\n--- Validation Error Handling ---")
try:
    # This will fail because 'pages' receives a string that cannot be turned into an integer
    invalid_book = Book(
        title="Invalid Book",
        author="Unknown",
        pages="not_a_number"
    )
except ValidationError as error:
    print("Pydantic caught a validation error:")
    print(error)
