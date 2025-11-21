from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError("Las contraseñas no coinciden")
        return v

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ReviewCreate(BaseModel):
    producto: str
    texto_resena: str

class ReviewResponse(BaseModel):
    id: int
    producto: str
    texto_resena: str
    sentimiento: Optional[str]
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True 