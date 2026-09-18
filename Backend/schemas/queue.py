from pydantic import BaseModel


class QueueCreate(BaseModel):
    service_id: int
    name: str