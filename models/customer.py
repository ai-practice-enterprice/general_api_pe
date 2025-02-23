from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    age: int
    email: str
    address: str
    phone: str


class Parcel(BaseModel):
    customer: Customer
    tracking_number: int
    weight: float
    destination: str
    recipient: str
