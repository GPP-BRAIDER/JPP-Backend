from pydantic import BaseModel

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str   
    age: int
    
    country: str
    city: str
    address: str
    postal_code: str
    phone_number : str

    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    age: int
    
    country: str
    city: str
    address: str
    postal_code: str
    phone_number : str

    class Config:
        orm_mode = True