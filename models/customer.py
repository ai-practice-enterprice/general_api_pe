from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    address: str
    city: str
    age: int
    email: str


class Package(BaseModel):
    customer: Customer
    status: str
    dimension: str
    weight: float
    destination_address: str
