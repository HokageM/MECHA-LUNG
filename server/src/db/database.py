from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Get DATABASE_URL from environment, with fallback for local development
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://lung_user:supersecret@localhost:5432/lung_db")

# If DATABASE_URL contains "db:" (Docker service name) but currently running locally, replace with localhost
if "db:" in DATABASE_URL and not os.getenv("DOCKER_ENV"):
    DATABASE_URL = DATABASE_URL.replace("db:", "localhost:")

Engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=Engine, autoflush=False, autocommit=False)
