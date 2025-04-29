from pydantic import BaseModel, EmailStr

from typing import Optional, List


class UserCreate(BaseModel):
    email: EmailStr

    password: str

    role: str


class UserLogin(BaseModel):
    email: EmailStr

    password: str


class Token(BaseModel):
    access_token: str

    token_type: str


class ParkingSlotCreate(BaseModel):
    slot_label: str


class ParkingSlotOut(BaseModel):
    id: int

    slot_label: str

    is_occupied: bool

    in_maintenance: bool

    class Config:
        orm_mode = True


class BookingCreate(BaseModel):
    slot_id: int


class BookingOut(BaseModel):
    id: int

    slot_id: int

    user_id: int

    class Config:
        orm_mode = True


class FeedbackCreate(BaseModel):
    booking_id: int

    message: str


class FeedbackOut(BaseModel):
    id: int

    booking_id: int

    message: str

    class Config:
        orm_mode = True
