from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):
    app_name: str = "Habit Tracker"
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    sender_email: EmailStr
    sender_password: str
    secret_key: str


    class Config:
        env_file = ".env"

settings = Settings()