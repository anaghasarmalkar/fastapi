from pydantic import BaseModel, Field, EmailStr

#  Pydantic schemas are about data validation and transfer, while SQLAlchemy models handle database interactions


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        # json_schema_extra = {
        #     "example": {
        #         "fullname": "Abdulazeez Abdulazeez Adeshina",
        #         "email": "abdulazeez@x.com",
        #         "password": "weakpassword"
        #     }
        # }
        from_attributes = True


class UserCreate(UserBase):
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@gmail.com",
                "password": "weakpassword"
            }
        }
        from_attributes = True


class UserResponse(UserBase):
    id: int
    email: str
    is_active: bool

    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    email: str
    password: str
    is_active: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    is_active: bool

    class Config:
        from_attributes = True


class UserLoginBase(UserBase):
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "x@x.com",
                "password": "weakpassword"
            }
        }
