from api.v1.routes import users, auth, habits, habit_logs
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(users.router, prefix="/user", tags=["Users"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(habits.router, prefix="/habit", tags=["Habit"])
api_router.include_router(habit_logs.router, prefix="/habit-log", tags=["Habit Log"])