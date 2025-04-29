from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from .. import models, schemas, database, auth

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/", response_model=schemas.FeedbackOut)
def submit_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(database.get_db),
                    current_user: models.User = Depends(auth.get_current_active_user)):
    booking = db.query(models.Booking).filter(models.Booking.id == feedback.booking_id,
                                              models.Booking.user_id == current_user.id).first()

    if not booking:
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    new_fb = models.Feedback(user_id=current_user.id, booking_id=feedback.booking_id, message=feedback.message)

    db.add(new_fb)

    db.commit()

    db.refresh(new_fb)

    return new_fb


@router.get("/", response_model=list[schemas.FeedbackOut])
def view_feedbacks(db: Session = Depends(database.get_db)):
    return db.query(models.Feedback).all()
