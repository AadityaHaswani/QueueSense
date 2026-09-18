from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select
from datetime import datetime, timezone

from models.service_session import ServiceSession

from database.session import SessionLocal
from models.queue import Queue
from models.service import Service
from schemas.queue import QueueCreate
from models.queue_entry import QueueEntry

router = APIRouter(prefix="/queues", tags=["Queues"])


@router.post("")
async def create_queue(queue_data: QueueCreate):
    db = SessionLocal()

    try:
        service = db.get(Service, queue_data.service_id)

        if not service:
            raise HTTPException(status_code=404, detail="Service not found")

        new_queue = Queue(service_id=queue_data.service_id, name=queue_data.name)

        db.add(new_queue)
        db.commit()
        db.refresh(new_queue)

        return {
            "id": new_queue.id,
            "service_id": new_queue.service_id,
            "name": new_queue.name,
            "status": new_queue.status,
            "current_token": new_queue.current_token,
        }

    finally:
        db.close()


@router.post("/{queue_id}/join")
async def join_queue(queue_id: int, user_id: int):
    db = SessionLocal()

    try:
        queue = db.execute(
            select(Queue).where(Queue.id == queue_id).with_for_update()
        ).scalar_one_or_none()

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")
        if queue.status != "active":
            raise HTTPException(
                status_code=400, detail="Queue is not accepting new customers"
            )

        existing_entry = db.execute(
            select(QueueEntry).where(
                QueueEntry.queue_id == queue_id,
                QueueEntry.user_id == user_id,
                QueueEntry.status == "waiting",
            )
        ).scalar_one_or_none()

        if existing_entry:
            raise HTTPException(status_code=400, detail="User is already in this queue")

        last_entry = (
            db.execute(
                select(QueueEntry)
                .where(QueueEntry.queue_id == queue_id)
                .order_by(QueueEntry.token_number.desc())
            )
            .scalars()
            .first()
        )

        if last_entry:
            token_number = last_entry.token_number + 1
        else:
            token_number = 1

        new_entry = QueueEntry(
            queue_id=queue_id,
            user_id=user_id,
            token_number=token_number,
            status="waiting",
        )

        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        return {
            "queue_id": queue_id,
            "user_id": user_id,
            "token_number": new_entry.token_number,
            "status": new_entry.status,
            "message": "Joined queue successfully",
        }

    finally:
        db.close()


@router.get("/{queue_id}/position/{token_number}")
async def get_queue_position(queue_id: int, token_number: int):
    db = SessionLocal()

    try:
        queue = db.get(Queue, queue_id)

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")

        people_ahead = db.scalar(
            select(func.count())
            .select_from(QueueEntry)
            .where(
                QueueEntry.queue_id == queue_id,
                QueueEntry.token_number < token_number,
                QueueEntry.status == "waiting",
            )
        )

        return {
            "queue_id": queue_id,
            "token_number": token_number,
            "people_ahead": people_ahead,
            "position": people_ahead + 1,
        }

    finally:
        db.close()


@router.delete("/{queue_id}/leave/{token_number}")
async def leave_queue(queue_id: int, token_number: int):
    db = SessionLocal()

    try:
        queue = db.get(Queue, queue_id)

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")

        entry = db.execute(
            select(QueueEntry).where(
                QueueEntry.queue_id == queue_id, QueueEntry.token_number == token_number
            )
        ).scalar_one_or_none()

        if not entry:
            raise HTTPException(status_code=404, detail="Queue entry not found")

        if entry.status != "waiting":
            raise HTTPException(
                status_code=400, detail="Only waiting customers can leave the queue"
            )

        entry.status = "cancelled"

        db.commit()

        return {
            "queue_id": queue_id,
            "token_number": token_number,
            "status": entry.status,
            "message": "Left queue successfully",
        }

    finally:
        db.close()


@router.get("/{queue_id}/status/{token_number}")
async def get_queue_status(queue_id: int, token_number: int):
    db = SessionLocal()

    try:
        # 1. Check if queue exists
        queue = db.get(Queue, queue_id)

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")

        # 2. Find the queue entry
        entry = db.execute(
            select(QueueEntry).where(
                QueueEntry.queue_id == queue_id, QueueEntry.token_number == token_number
            )
        ).scalar_one_or_none()

        if not entry:
            raise HTTPException(status_code=404, detail="Queue entry not found")

        # 3. If customer is still waiting, calculate position
        if entry.status == "waiting":

            people_ahead = db.scalar(
                select(func.count())
                .select_from(QueueEntry)
                .where(
                    QueueEntry.queue_id == queue_id,
                    QueueEntry.token_number < token_number,
                    QueueEntry.status == "waiting",
                )
            )

            position = people_ahead + 1

        else:
            people_ahead = 0
            position = None

        # 4. Return complete queue status
        return {
            "queue_id": queue_id,
            "token_number": token_number,
            "status": entry.status,
            "people_ahead": people_ahead,
            "position": position,
            "current_token": queue.current_token,
        }

    finally:
        db.close()


@router.post("/{queue_id}/call-next")
async def call_next_customer(queue_id: int):
    db = SessionLocal()

    try:
        # Check whether the queue exists
        queue = db.get(Queue, queue_id)

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")
        if queue.status != "active":
            raise HTTPException(status_code=400, detail="Queue is not active")

        # Find the first waiting customer
        entry = (
            db.execute(
                select(QueueEntry)
                .where(QueueEntry.queue_id == queue_id, QueueEntry.status == "waiting")
                .order_by(QueueEntry.token_number)
            )
            .scalars()
            .first()
        )

        # No customer is waiting
        if not entry:
            raise HTTPException(status_code=400, detail="No customers waiting")

        # Change customer state
        entry.status = "called"

        # Update queue's current token
        queue.current_token = entry.token_number

        db.commit()

        return {
            "queue_id": queue_id,
            "token_number": entry.token_number,
            "status": entry.status,
            "message": "Next customer called",
        }

    finally:
        db.close()


@router.post("/{queue_id}/serve/{token_number}")
async def serve_customer(queue_id: int, token_number: int):
    db = SessionLocal()

    try:
        # 1. Check whether queue exists
        queue = db.get(Queue, queue_id)

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")

        # 2. Find the queue entry
        entry = db.execute(
            select(QueueEntry).where(
                QueueEntry.queue_id == queue_id, QueueEntry.token_number == token_number
            )
        ).scalar_one_or_none()

        if not entry:
            raise HTTPException(status_code=404, detail="Queue entry not found")

        # 3. Only a called customer can be served
        if entry.status != "serving":
            raise HTTPException(
                status_code=400,
                detail="Only a customer currently being served can be completed",
            )
        service_session = db.execute(
            select(ServiceSession).where(ServiceSession.queue_entry_id == entry.id)
        ).scalar_one_or_none()
        if not service_session:
            raise HTTPException(status_code=400, detail="Service session not found")
        entry.status = "served"
        service_session.completed_at = datetime.now(timezone.utc)

        db.commit()

        return {
            "queue_id": queue_id,
            "token_number": token_number,
            "status": entry.status,
            "message": "Customer served successfully",
        }

    finally:
        db.close()


@router.post("/{queue_id}/skip/{token_number}")
async def skip_customer(queue_id: int, token_number: int):
    db = SessionLocal()

    try:
        # 1. Check whether queue exists
        queue = db.get(Queue, queue_id)

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")

        # 2. Find the queue entry
        entry = db.execute(
            select(QueueEntry).where(
                QueueEntry.queue_id == queue_id, QueueEntry.token_number == token_number
            )
        ).scalar_one_or_none()

        if not entry:
            raise HTTPException(status_code=404, detail="Queue entry not found")

        # 3. Only a called customer can be marked as no-show
        if entry.status != "called":
            raise HTTPException(
                status_code=400,
                detail="Only a called customer can be marked as no-show",
            )

        # 4. Change the status
        entry.status = "no_show"

        # 5. Save the change
        db.commit()

        return {
            "queue_id": queue_id,
            "token_number": token_number,
            "status": entry.status,
            "message": "Customer marked as no-show",
        }

    finally:
        db.close()


@router.patch("/{queue_id}/pause")
async def pause_queue(queue_id: int):
    db = SessionLocal()

    try:
        queue = db.get(Queue, queue_id)

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")

        if queue.status == "closed":
            raise HTTPException(status_code=400, detail="Closed queue cannot be paused")

        if queue.status == "paused":
            raise HTTPException(status_code=400, detail="Queue is already paused")

        queue.status = "paused"

        db.commit()

        return {
            "queue_id": queue.id,
            "status": queue.status,
            "message": "Queue paused successfully",
        }

    finally:
        db.close()


@router.patch("/{queue_id}/resume")
async def resume_queue(queue_id: int):
    db = SessionLocal()

    try:
        queue = db.get(Queue, queue_id)

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")

        if queue.status == "closed":
            raise HTTPException(
                status_code=400, detail="Closed queue cannot be resumed"
            )

        if queue.status == "active":
            raise HTTPException(status_code=400, detail="Queue is already active")

        queue.status = "active"

        db.commit()

        return {
            "queue_id": queue.id,
            "status": queue.status,
            "message": "Queue resumed successfully",
        }

    finally:
        db.close()


@router.patch("/{queue_id}/close")
async def close_queue(queue_id: int):
    db = SessionLocal()

    try:
        queue = db.get(Queue, queue_id)

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")

        if queue.status == "closed":
            raise HTTPException(status_code=400, detail="Queue is already closed")

        queue.status = "closed"

        db.commit()

        return {
            "queue_id": queue.id,
            "status": queue.status,
            "message": "Queue closed successfully",
        }

    finally:
        db.close()


@router.post("/{queue_id}/start-service/{token_number}")
async def start_service(queue_id: int, token_number: int):
    db = SessionLocal()

    try:
        queue = db.get(Queue, queue_id)

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")

        entry = db.execute(
            select(QueueEntry).where(
                QueueEntry.queue_id == queue_id, QueueEntry.token_number == token_number
            )
        ).scalar_one_or_none()

        if not entry:
            raise HTTPException(status_code=404, detail="Queue entry not found")

        if entry.status != "called":
            raise HTTPException(
                status_code=400, detail="Only a called customer can start service"
            )

        entry.status = "serving"

        service_session = ServiceSession(
            queue_entry_id=entry.id, started_at=datetime.now(timezone.utc)
        )

        db.add(service_session)
        db.commit()
        db.refresh(service_session)

        return {
            "queue_id": queue_id,
            "token_number": token_number,
            "status": entry.status,
            "started_at": service_session.started_at,
            "message": "Service started successfully",
        }

    finally:
        db.close()


@router.get("/{queue_id}/eta/{token_number}")
async def get_queue_eta(queue_id: int, token_number: int):
    db = SessionLocal()

    try:
        # 1. Check whether queue exists
        queue = db.get(Queue, queue_id)

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")

        # 2. Check whether the token exists
        entry = db.execute(
            select(QueueEntry).where(
                QueueEntry.queue_id == queue_id, QueueEntry.token_number == token_number
            )
        ).scalar_one_or_none()

        if not entry:
            raise HTTPException(status_code=404, detail="Queue entry not found")

        # 3. Count people ahead
        people_ahead = db.scalar(
            select(func.count())
            .select_from(QueueEntry)
            .where(
                QueueEntry.queue_id == queue_id,
                QueueEntry.token_number < token_number,
                QueueEntry.status == "waiting",
            )
        )

        # 4. Calculate average service time in seconds
        average_seconds = db.scalar(
            select(
                func.avg(
                    func.extract(
                        "epoch", ServiceSession.completed_at - ServiceSession.started_at
                    )
                )
            )
            .select_from(ServiceSession)
            .join(QueueEntry, ServiceSession.queue_entry_id == QueueEntry.id)
            .where(
                QueueEntry.queue_id == queue_id,
                ServiceSession.completed_at.is_not(None),
            )
        )

        # 5. Handle case where no service history exists
        if average_seconds is None:
            average_service_time_minutes = None
            estimated_wait_minutes = None

        else:
            average_service_time_minutes = average_seconds / 60
            estimated_wait_minutes = people_ahead * average_service_time_minutes

        return {
            "queue_id": queue_id,
            "token_number": token_number,
            "people_ahead": people_ahead,
            "average_service_time_minutes": (
                round(average_service_time_minutes, 2)
                if average_service_time_minutes is not None
                else None
            ),
            "estimated_wait_minutes": (
                round(estimated_wait_minutes, 2)
                if estimated_wait_minutes is not None
                else None
            ),
        }

    finally:
        db.close()


@router.get("/{queue_id}/stats")
async def get_queue_stats(queue_id: int):
    db = SessionLocal()

    try:
        # 1. Check whether queue exists
        queue = db.get(Queue, queue_id)

        if not queue:
            raise HTTPException(status_code=404, detail="Queue not found")

        # 2. Count total customers
        total_customers = db.scalar(
            select(func.count())
            .select_from(QueueEntry)
            .where(QueueEntry.queue_id == queue_id)
        )

        # 3. Count waiting customers
        waiting = db.scalar(
            select(func.count())
            .select_from(QueueEntry)
            .where(QueueEntry.queue_id == queue_id, QueueEntry.status == "waiting")
        )

        # 4. Count called customers
        called = db.scalar(
            select(func.count())
            .select_from(QueueEntry)
            .where(QueueEntry.queue_id == queue_id, QueueEntry.status == "called")
        )

        # 5. Count customers currently being served
        serving = db.scalar(
            select(func.count())
            .select_from(QueueEntry)
            .where(QueueEntry.queue_id == queue_id, QueueEntry.status == "serving")
        )

        # 6. Count served customers
        served = db.scalar(
            select(func.count())
            .select_from(QueueEntry)
            .where(QueueEntry.queue_id == queue_id, QueueEntry.status == "served")
        )

        # 7. Count cancelled customers
        cancelled = db.scalar(
            select(func.count())
            .select_from(QueueEntry)
            .where(QueueEntry.queue_id == queue_id, QueueEntry.status == "cancelled")
        )

        # 8. Count no-show customers
        no_show = db.scalar(
            select(func.count())
            .select_from(QueueEntry)
            .where(QueueEntry.queue_id == queue_id, QueueEntry.status == "no_show")
        )

        return {
            "queue_id": queue_id,
            "total_customers": total_customers,
            "waiting": waiting,
            "called": called,
            "serving": serving,
            "served": served,
            "cancelled": cancelled,
            "no_show": no_show,
        }

    finally:
        db.close()
