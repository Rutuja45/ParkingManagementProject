from fastapi import FastAPI
from .database import Base, engine
from .routers import auth, parking, booking, feedback

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(parking.router)
app.include_router(booking.router)
app.include_router(feedback.router)


@app.get("/")
def root():
   return {"message": "Parking Management System API is running"}