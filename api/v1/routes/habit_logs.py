"""habit_logs module"""

"""Endpoints
POST api/v1/habit/log - logs habit
GET api/v1/habit/log - gets all logs of authenticated customer
GET api/v1/habit/log/{id} - gets specific log of authenticated customer
PATCH api/v1/habit/log/{id} - update status
DELETE api/v1/habit/log/{id} - delete log
"""
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import date
from schemas.utils.enums import StatusEnum
from schemas.schema import Habit_log, Habit, User
from sqlalchemy.exc import NoResultFound
from typing import Annotated
from .auth import get_current_user
from config.db import session

router = APIRouter()

class CeateLog(BaseModel):
    date: date
    status: StatusEnum

@router.post("/log/{habit_id}", status_code=status.HTTP_201_CREATED)
def log_habit(habit_id, current_user: Annotated[User, Depends(get_current_user)], body_data: CeateLog):
    try:
        habit = session.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
        if not habit:
            raise NoResultFound
        new_log = Habit_log(
            date=body_data.date,
            status=body_data.status,
            habit_id=habit_id
        )
        session.add(new_log)
        session.commit()
        return {
            "message": "Habit logged successfully"
        }
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "resource not found"}
        )