from sqlalchemy import create_engine
from config.config import settings
from sqlalchemy.orm import sessionmaker

DB_USER = settings.db_user
DB_PASSWORD = settings.db_password
DB_HOST = settings.db_host
DB_PORT = settings.db_port
DB_DATABASE = settings.db_name

engine = create_engine(f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")

Session = sessionmaker(bind=engine)
session = Session()