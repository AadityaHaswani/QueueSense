from fastapi import APIRouter,HTTPException
from sqlalchemy import select

from database.session import SessionLocal
from models.organization import Organization
from schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
)

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("", response_model=OrganizationResponse)
async def create_organization(organization_data: OrganizationCreate):
    db = SessionLocal()

    try:
        new_organization = Organization(name=organization_data.name)

        db.add(new_organization)
        db.commit()
        db.refresh(new_organization)

        return new_organization

    finally:
        db.close()
@router.get("", response_model=list[OrganizationResponse])
async def get_organizations():
    db = SessionLocal()

    try:
        result = db.execute(
            select(Organization)
        )

        organizations = result.scalars().all()

        return organizations

    finally:
        db.close()

@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse
)
async def get_organization(organization_id: int):
    db = SessionLocal()

    try:
        organization = db.get(
            Organization,
            organization_id
        )

        if not organization:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        return organization

    finally:
        db.close()