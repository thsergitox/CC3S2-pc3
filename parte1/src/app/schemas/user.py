from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
