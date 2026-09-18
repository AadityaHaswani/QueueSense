from pydantic import BaseModel


class BranchCreate(BaseModel):
    organization_id: int
    name: str


class BranchResponse(BaseModel):
    id: int
    organization_id: int
    name: str
    status: str