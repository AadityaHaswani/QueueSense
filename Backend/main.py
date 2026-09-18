from fastapi import FastAPI
from pydantic import BaseModel
from schemas.queue import QueueCreate
from database.session import SessionLocal
from models.queue import Queue
from sqlalchemy import select
from models.queue_entry import QueueEntry
from models.organization import Organization
from models.branch import Branch
from models.service import Service

from routes.organization import router as organization_router
from routes.branch import router as branch_router
from routes.service import router as service_router
from routes.queue import router as queue_router
app = FastAPI()

app.include_router(organization_router)
app.include_router(branch_router)
app.include_router(service_router)
app.include_router(queue_router)
@app.get("/")
async def greet():
    return {"message": "Hello QueueSense"}


@app.get("/queues")
async def get_queues():
    db = SessionLocal()

    try:
        result = db.execute(select(Queue))
        queues = result.scalars().all()

        return queues

    finally:
        db.close()


@app.get("/queues/{queue_id}")
async def get_queue(queue_id: int):
    return {"queue_id": queue_id}


@app.get("/queues")
async def get_queues(status: str = "active"):
    return {"status": status}


class JoinQueueRequest(BaseModel):
    user_id: int



