from pydantic import BaseModel, EmailStr, Field 

class UserResponse(BaseModel):
    """Schema for user response"""
    id: int 
    email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config:
        arm_mode = True 


        