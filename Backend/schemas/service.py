from pydantic import BaseModel


class ServiceCreate(BaseModel):
    branch_id: int
    name: str


class ServiceResponse(BaseModel):
    id: int
    branch_id: int
    name: str
    status: str