from pydantic import BaseModel

class Country(BaseModel):
    country_name: str
    
