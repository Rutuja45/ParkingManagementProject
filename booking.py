from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth
router = APIRouter(prefix="/booking", tags=["Booking"])


@router.post("/", response_model=schemas.BookingOut)
def book_slot(booking: schemas.BookingCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
   slot = db.query(models.ParkingSlot).filter(models.ParkingSlot.id == booking.slot_id, models.ParkingSlot.is_occupied == False, models.ParkingSlot.in_maintenance == False).first()
   if not slot:
       raise HTTPException(status_code=400, detail="Slot unavailable")
   slot.is_occupied = True
   new_booking = models.Booking(user_id=current_user.id, slot_id=booking.slot_id)
   db.add(new_booking)
   db.commit()
   db.refresh(new_booking)
   return new_booking

@router.get("/", response_model=list[schemas.BookingOut])
def get_my_bookings(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
   return db.query(models.Booking).filter(models.Booking.user_id == current_user.id).all()


@router.delete("/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
   booking = db.query(models.Booking).filter(models.Booking.id == booking_id, models.Booking.user_id == current_user.id).first()
   if not booking:
       raise HTTPException(status_code=404, detail="Booking not found")
   slot = db.query(models.ParkingSlot).filter(models.ParkingSlot.id == booking.slot_id).first()
   slot.is_occupied = False
   db.delete(booking)
   db.commit()
   return {"message": "Booking canceled"}