from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Todoitem(Base):
    __tablename__ = "tasks"  # Replace with your actual table name

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)
    status = Column(String, default="todo")  # Can be "todo", "in-progress", or "completed"

    def __repr__(self):
        return f"<Todoitem(id={self.id}, title={self.title}, completed={self.completed}, status={self.status})>"
# Pydantic model for input validation and serialization
class TodoitemCreate(BaseModel):
    title: str
    completed: bool = False
    status: str = "todo"

# Pydantic model for output serialization, including the ID
class TodoitemResponse(TodoitemCreate):
    id: int

    class Config:
        orm_mode = True  # This allows Pydantic to work with SQLAlchemy ORM models    
