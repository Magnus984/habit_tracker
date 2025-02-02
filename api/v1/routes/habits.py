"""habits module"""

"""Endpoints
POST api/v1/habit/new - create a habit
GET api/v1/habit - get all habits of authenticated user add pagination
GET api/v1/habit{habit_id} - get a specific habit of authenticated user
PUT api/v1/habit/{habit_id} - update habit(description, remindertime, frequency)
DELETE api/v1/habit/{habit_id} - remove habit of authenticated user
"""
from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import time
from schemas.schema import Habit, User
from config.db import session
from .auth import get_current_user
from typing import Annotated, List
from sqlalchemy.exc import NoResultFound
from typing import Optional

router = APIRouter()

class CreateHabit(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the habit", max_length=400
    )
    frequency: str
    reminder_time: time

class GetHabitResponse(BaseModel):
    id: int
    name: str
    description: str
    frequency: str

class UpdateHabit(BaseModel):
    name: str
    description: str
    frequency: str
    reminder_time: Optional[time] = None


@router.post("/new", status_code=status.HTTP_201_CREATED)
def create_habit(habit_data: CreateHabit,  current_user: Annotated[User, Depends(get_current_user)]):
    try:
        new_habit = Habit(
            name=habit_data.name,
            description=habit_data.description,
            frequency=habit_data.frequency,
            reminder_time=habit_data.reminder_time,
            user_id=current_user.id
        )
        session.add(new_habit)
        session.commit()
        return {
            "message": f"{new_habit.name} created successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[GetHabitResponse])
def get_all_habits(current_user: Annotated[User, Depends(get_current_user)]):
    try:
        habits = session.query(Habit).filter(Habit.user_id==current_user.id).all()
        habit_response = [GetHabitResponse(
            id=habit.id,
            name=habit.name,
            description=habit.description,
            frequency=habit.frequency
        ) for habit in habits]
        return habit_response
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/{habit_id}", status_code=status.HTTP_200_OK)
def get_one(habit_id, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        habit = session.query(Habit).filter(Habit.user_id==current_user.id, Habit.id==habit_id).first()
        if not habit:
            raise NoResultFound
        new_response = GetHabitResponse(
            id=habit.id,
            name=habit.name,
            description=habit.description,
            frequency=habit.frequency
        )
        return new_response
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

@router.put("/{habit_id}", status_code=status.HTTP_200_OK)
def update_habit(habit_id, update_data: UpdateHabit, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        habit = session.query(Habit).filter(Habit.user_id == current_user.id, Habit.id == habit_id).first()
        if not habit:
            raise NoResultFound
        habit.name = update_data.name
        habit.description = update_data.description
        habit.frequency = update_data.frequency
        if update_data.reminder_time is not None:
            habit.reminder_time = update_data.reminder_time
        session.commit()
        session.refresh(habit)
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

@router.delete("/{habit_id}", status_code=status.HTTP_200_OK)
def remove_habit(habit_id, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        habit = session.query(Habit).filter(Habit.user_id == current_user.id, Habit.id == habit_id).first()
        if not habit:
            raise NoResultFound
        session.delete(habit)
        session.commit()
        return {
            "message": "Habit Deleted"
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