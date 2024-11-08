from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from model import Base
import os

#DATABASE_URL = "postgresql+asyncpg://todolist_owner:8nyOBat6KpHj@ep-wandering-water-a5y71uyx.us-east-2.aws.neon.tech/todolist"
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the environment.")
# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Initialize the database
async def init_db():
    async with engine.begin() as conn:
        # Create all tables in the engine
        await conn.run_sync(Base.metadata.create_all)
