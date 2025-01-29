from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Date, Time, ForeignKey, Sequence, Enum as SqlEnum
from .utils.enums import StatusEnum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(16), nullable=False)
    password_hash = Column(String(16), nullable=False)
    email = Column(String(60), nullable=False, unique=True)


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, Sequence('habit_id_seq'), primary_key=True)
    name = Column(String(60), nullable=False)
    description = Column(String(255), nullable=False)
    frequency = Column(Integer, nullable=False)
    reminder_time = Column(Time(timezone=False), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))


class Habit_log(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, Sequence('habit_log_id_seq'), primary_key=True)
    date = Column(Date, nullable=False)
    status = Column(SqlEnum(StatusEnum), nullable=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
