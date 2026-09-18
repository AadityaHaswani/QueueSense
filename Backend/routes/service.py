from fastapi import APIRouter, HTTPException

from database.session import SessionLocal
from models.branch import Branch
from models.service import Service
from schemas.service import ServiceCreate, ServiceResponse
from sqlalchemy import select
from models.queue import Queue


router = APIRouter(
    prefix="/services",
    tags=["Services"]
)

@router.post("", response_model=ServiceResponse)
async def create_service(service_data: ServiceCreate):
    db = SessionLocal()

    try:
        branch = db.get(
            Branch,
            service_data.branch_id
        )

        if not branch:
            raise HTTPException(
                status_code=404,
                detail="Branch not found"
            )

        new_service = Service(
            branch_id=service_data.branch_id,
            name=service_data.name
        )

        db.add(new_service)
        db.commit()
        db.refresh(new_service)

        return new_service

    finally:
        db.close()
@router.get("", response_model=list[ServiceResponse])
async def get_services(branch_id: int | None = None):
    db = SessionLocal()

    try:
        query = select(Service)

        if branch_id is not None:
            query = query.where(
                Service.branch_id == branch_id
            )

        result = db.execute(query)

        services = result.scalars().all()

        return services

    finally:
        db.close()

@router.get(
    "/{service_id}",
    response_model=ServiceResponse
)
async def get_service(service_id: int):
    db = SessionLocal()

    try:
        service = db.get(
            Service,
            service_id
        )

        if not service:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        return service

    finally:
        db.close()

@router.get(
    "/{service_id}/queues"
)
async def get_service_queues(service_id: int):
    db = SessionLocal()

    try:
        service = db.get(
            Service,
            service_id
        )

        if not service:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        query = select(Queue).where(
            Queue.service_id == service_id
        )

        result = db.execute(query)

        queues = result.scalars().all()

        return queues

    finally:
        db.close()