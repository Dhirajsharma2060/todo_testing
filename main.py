import logging
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from database import init_db, AsyncSessionLocal, engine  # Import `engine` here
from model import TodoitemCreate, TodoitemResponse
from crud import add_task, get_all_tasks, get_task, update_task, delete_task

# Set SQLAlchemy engine logging to WARNING to suppress detailed query output
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)  # <-- Logging level change

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get the DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup_event():
    await init_db()  # Initialize the database

@app.on_event("shutdown")
async def shutdown_event():
    # Properly close the engine on shutdown
    await engine.dispose()

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API Endpoints
@app.get("/task", response_model=list[TodoitemResponse])
async def read_all_tasks(db: AsyncSession = Depends(get_db)):
    return await get_all_tasks(db)

@app.get("/task/{id}", response_model=TodoitemResponse)
async def read_task(id: int, db: AsyncSession = Depends(get_db)):
    item = await get_task(db, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="Todo item not found")

@app.post("/task", response_model=TodoitemResponse)
async def create_todos(item: TodoitemCreate, db: AsyncSession = Depends(get_db)):
    return await add_task(db, item)

@app.delete("/task/{id}")
async def delete_todos(id: int, db: AsyncSession = Depends(get_db)):
    if await delete_task(db, id):
        return {"message": "Todo item deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/task/{id}", response_model=TodoitemResponse)
async def update_todos(id: int, item: TodoitemCreate, db: AsyncSession = Depends(get_db)):
    updated_item = await update_task(db, id, item)
    if updated_item:
        return updated_item
    raise HTTPException(status_code=404, detail="Task not found")
