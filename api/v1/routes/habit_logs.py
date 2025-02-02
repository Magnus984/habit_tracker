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

class CreateLog(BaseModel):
    date: date
    status: StatusEnum

class GetLog(BaseModel):
    id: int
    date: date
    status: StatusEnum

class UpdateLog(BaseModel):
    status: StatusEnum

@router.post("{habit_id}", status_code=status.HTTP_201_CREATED)
def log_habit(habit_id, current_user: Annotated[User, Depends(get_current_user)], body_data: CreateLog):
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

@router.get("/all", status_code=status.HTTP_200_OK)
def get_all_logs(current_user: Annotated[User, Depends(get_current_user)]):
    print("I am inside the endpoint")
    try:
        habit_logs = (
            session.query(Habit_log)
            .join(Habit, Habit_log.habit_id == Habit.id)
            .filter(Habit.user_id == current_user.id)
            .all()
        )
        if not habit_logs:
            raise NoResultFound
        habit_log_response = [GetLog(
            id=habit_log.id,
            date=habit_log.date,
            status=habit_log.status
        ) for habit_log in habit_logs]
        return habit_log_response
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "resource cannot be found"}
        )
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/{habit_log_id}", status_code=status.HTTP_200_OK)
def get_one(habit_log_id, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        habit_log = (
            session.query(Habit_log)
            .join(Habit, Habit_log.habit_id == Habit.id)
            .filter(Habit.user_id == current_user.id, Habit_log.id == habit_log_id)
            .one()
        )
        return GetLog(
            id=habit_log.id,
            date=habit_log.date,
            status=habit_log.status
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "resource cannot be found"}
        )
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.patch("/habit_log_id", status_code=status.HTTP_200_OK)
def update_status(habit_log_id, body_data: UpdateLog, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        habit_log = session.query(Habit_log).filter(Habit_log.id == habit_log_id).one()
        habit_log.status = body_data.status
        session.commit()
        session.refresh(habit_log)
        return {
            "message": "Update done successfully"
        }
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "resource cannot be found"}
        )
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.delete("/habit_log_id", status_code=status.HTTP_200_OK)
def remove_log(habit_log_id, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        habit_log = session.query(Habit_log).filter(Habit_log.id == habit_log_id).one()
        session.delete(habit_log)
        session.commit()
        return {
            "message": "Habit Log Deleted"
        }
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "resource cannot be found"}
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )