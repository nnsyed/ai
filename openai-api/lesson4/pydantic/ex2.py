from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr

# Valid email
user = User(name="Alice", email="alice@example.com")
print(user.email) #> alice@example.com

#user1 = User(name="Alice1", email="salman@example.com")


# pip install 'pydantic[email]'
# Invalid email raises a ValidationError
# invalid_user = User(name="Bob", email="not-an-email")
