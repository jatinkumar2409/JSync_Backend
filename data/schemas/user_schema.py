from pydantic import BaseModel

class User_Schema(BaseModel):
    id : str
    name : str
    email : str
    password : str
    profile : str

class Sign_Up_Request(BaseModel):
    name : str
    email : str
    password : str

class Sign_In_Request(BaseModel):
    email : str
    password : str