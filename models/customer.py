from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    age: int
    email: str
    address: str
    phone: str
