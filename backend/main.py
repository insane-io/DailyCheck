from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from backend import database
import random

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/daily-tasks")
def get_daily_tasks(db: Session = Depends(get_db)):
    today = datetime.today().weekday()
    day_type = "weekend" if today >= 5 else "weekday"
    
    tasks = db.query(database.Task).filter(database.Task.day_type == day_type).all()
    
    if not tasks:
        return {"message": "No tasks in the database yet!"}
    
    todays_plate = random.sample(tasks, min(len(tasks), 2))
    return {"day_type": day_type, "tasks": todays_plate}