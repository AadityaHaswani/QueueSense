from fastapi import APIRouter, HTTPException
from database.session import SessionLocal
from models.branch import Branch
from models.organization import Organization
from sqlalchemy import select
from schemas.branch import BranchCreate, BranchResponse

router = APIRouter(
    prefix="/branches",
    tags=["Branches"]
)

@router.post("", response_model=BranchResponse)
async def create_branch(branch_data: BranchCreate):
    db = SessionLocal()

    try:
        organization = db.get(
            Organization,
            branch_data.organization_id
        )

        if not organization:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        new_branch = Branch(
            organization_id=branch_data.organization_id,
            name=branch_data.name
        )

        db.add(new_branch)
        db.commit()
        db.refresh(new_branch)

        return new_branch

    finally:
        db.close()
@router.get("", response_model=list[BranchResponse])
async def get_branches(organization_id: int | None = None):
    db = SessionLocal()

    try:
        query = select(Branch)

        if organization_id is not None:
            query = query.where(
                Branch.organization_id == organization_id
            )

        result = db.execute(query)

        branches = result.scalars().all()

        return branches

    finally:
        db.close()

@router.get(
    "/{branch_id}",
    response_model=BranchResponse
)
async def get_branch(branch_id: int):
    db = SessionLocal()

    try:
        branch = db.get(
            Branch,
            branch_id
        )

        if not branch:
            raise HTTPException(
                status_code=404,
                detail="Branch not found"
            )

        return branch

    finally:
        db.close()