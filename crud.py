from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model import Todoitem, TodoitemCreate

async def add_task(db: AsyncSession, item: TodoitemCreate):
    todo_item = Todoitem(**item.dict())
    db.add(todo_item)
    await db.commit()
    await db.refresh(todo_item)
    return todo_item

async def get_all_tasks(db: AsyncSession):
    result = await db.execute(select(Todoitem))
    return result.scalars().all()

async def get_task(db: AsyncSession, id: int):
    result = await db.execute(select(Todoitem).where(Todoitem.id == id))
    return result.scalar_one_or_none()

async def update_task(db: AsyncSession, id: int, item: TodoitemCreate):
    existing_item = await get_task(db, id)
    if existing_item:
        for key, value in item.dict().items():
            setattr(existing_item, key, value)
        await db.commit()
        await db.refresh(existing_item)
        return existing_item
    return None

async def delete_task(db: AsyncSession, id: int):
    existing_item = await get_task(db, id)
    if existing_item:
        await db.delete(existing_item)
        await db.commit()
        return True
    return False
