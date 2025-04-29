from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)

    password = Column(String)

    role = Column(String, default="user")  # user or admin

    bookings = relationship("Booking", back_populates="user")

    feedbacks = relationship("Feedback", back_populates="user")


class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True)

    slot_label = Column(String, unique=True)

    is_occupied = Column(Boolean, default=False)

    in_maintenance = Column(Boolean, default=False)

    bookings = relationship("Booking", back_populates="slot")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    slot_id = Column(Integer, ForeignKey("parking_slots.id"))

    user = relationship("User", back_populates="bookings")

    slot = relationship("ParkingSlot", back_populates="bookings")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    booking_id = Column(Integer, ForeignKey("bookings.id"))

    message = Column(String)

    user = relationship("User", back_populates="feedbacks")
