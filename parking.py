from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from .. import models, schemas, database, auth

router = APIRouter(prefix="/parking", tags=["Parking Slots"])


@router.post("/", response_model=schemas.ParkingSlotOut)
def create_parking_slot(slot: schemas.ParkingSlotCreate, db: Session = Depends(database.get_db),admin_user: models.User = Depends(auth.get_admin_user)):
    db_slot = models.ParkingSlot(slot_label=slot.slot_label)

    db.add(db_slot)

    db.commit()

    db.refresh(db_slot)

    return db_slot


@router.get("/", response_model=list[schemas.ParkingSlotOut])
def get_all_slots(db: Session = Depends(database.get_db)):
    return db.query(models.ParkingSlot).all()


@router.put("/{slot_id}")
def update_slot(slot_id: int, in_maintenance: bool, db: Session = Depends(database.get_db),
                admin_user: models.User = Depends(auth.get_admin_user)):
    slot = db.query(models.ParkingSlot).filter(models.ParkingSlot.id == slot_id).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    slot.in_maintenance = in_maintenance

    db.commit()

    return {"message": "Slot updated"}


@router.delete("/{slot_id}")
def delete_slot(slot_id: int, db: Session = Depends(database.get_db)):
    slot = db.query(models.ParkingSlot).filter(models.ParkingSlot.id == slot_id).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    db.delete(slot)

    db.commit()

    return {"message": "Slot deleted"}
