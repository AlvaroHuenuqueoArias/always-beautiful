from datetime import date
from typing import List
from uuid import UUID

from fastapi import APIRouter, status

from app.schedule.repository import ScheduleRepository
from app.schedule.schemas import (
    DateBlockCreate,
    DateBlockResponse,
    DayScheduleResponse,
    DeleteDateBlockResponse,
    ScheduleTemplateResponse,
    ScheduleTemplateUpdate,
)
from app.schedule.service import ScheduleService

router = APIRouter(prefix="/schedule", tags=["schedule"])

schedule_repository = ScheduleRepository()
schedule_service = ScheduleService(schedule_repository)


@router.get("/health", status_code=status.HTTP_200_OK)
def schedule_health():
    return {
        "status": "ok",
        "module": "schedule",
    }


@router.get(
    "/template",
    response_model=ScheduleTemplateResponse,
    status_code=status.HTTP_200_OK,
)
def get_schedule_template() -> ScheduleTemplateResponse:
    return schedule_service.get_schedule_template()


@router.put(
    "/template",
    response_model=ScheduleTemplateResponse,
    status_code=status.HTTP_200_OK,
)
def replace_schedule_template(
    payload: ScheduleTemplateUpdate,
) -> ScheduleTemplateResponse:
    return schedule_service.replace_schedule_template(payload)


@router.get(
    "/blocks",
    response_model=List[DateBlockResponse],
    status_code=status.HTTP_200_OK,
)
def list_date_blocks() -> List[DateBlockResponse]:
    return schedule_service.list_date_blocks()


@router.post(
    "/blocks",
    response_model=DateBlockResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_date_block(payload: DateBlockCreate) -> DateBlockResponse:
    return schedule_service.create_date_block(payload)


@router.delete(
    "/blocks/{block_id}",
    response_model=DeleteDateBlockResponse,
    status_code=status.HTTP_200_OK,
)
def delete_date_block(block_id: UUID) -> DeleteDateBlockResponse:
    schedule_service.delete_date_block(block_id)

    return DeleteDateBlockResponse(
        deleted=True,
        block_id=block_id,
    )


@router.get(
    "/day/{target_date}",
    response_model=DayScheduleResponse,
    status_code=status.HTTP_200_OK,
)
def get_day_schedule(target_date: date) -> DayScheduleResponse:
    return schedule_service.get_day_schedule(target_date)