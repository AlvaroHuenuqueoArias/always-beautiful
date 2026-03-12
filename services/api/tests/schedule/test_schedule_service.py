from datetime import date, time

import pytest
from fastapi import HTTPException

from app.schedule.repository import ScheduleRepository
from app.schedule.schemas import (
    DateBlockCreate,
    DailyBreak,
    ScheduleTemplateUpdate,
    WeeklyScheduleRule,
)
from app.schedule.service import ScheduleService


def build_service() -> ScheduleService:
    repository = ScheduleRepository()
    return ScheduleService(repository)


def valid_template() -> ScheduleTemplateUpdate:
    return ScheduleTemplateUpdate(
        weekly_rules=[
            WeeklyScheduleRule(
                day_of_week=0,
                is_working_day=True,
                start_time=time(11, 0),
                end_time=time(19, 0),
            ),
            WeeklyScheduleRule(
                day_of_week=1,
                is_working_day=True,
                start_time=time(11, 0),
                end_time=time(19, 0),
            ),
        ],
        breaks=[
            DailyBreak(
                day_of_week=0,
                start_time=time(14, 0),
                end_time=time(15, 0),
                label="Lunch",
            ),
        ],
    )


def test_replace_schedule_template_success():
    service = build_service()
    result = service.replace_schedule_template(valid_template())

    assert len(result.weekly_rules) == 2
    assert len(result.breaks) == 1


def test_replace_schedule_template_rejects_break_outside_work_window():
    service = build_service()

    payload = ScheduleTemplateUpdate(
        weekly_rules=[
            WeeklyScheduleRule(
                day_of_week=0,
                is_working_day=True,
                start_time=time(11, 0),
                end_time=time(19, 0),
            ),
        ],
        breaks=[
            DailyBreak(
                day_of_week=0,
                start_time=time(10, 30),
                end_time=time(11, 30),
                label="Invalid break",
            ),
        ],
    )

    with pytest.raises(HTTPException) as exc:
        service.replace_schedule_template(payload)

    assert exc.value.status_code == 400


def test_replace_schedule_template_rejects_overlapping_breaks():
    service = build_service()

    payload = ScheduleTemplateUpdate(
        weekly_rules=[
            WeeklyScheduleRule(
                day_of_week=0,
                is_working_day=True,
                start_time=time(11, 0),
                end_time=time(19, 0),
            ),
        ],
        breaks=[
            DailyBreak(
                day_of_week=0,
                start_time=time(14, 0),
                end_time=time(15, 0),
                label="Break A",
            ),
            DailyBreak(
                day_of_week=0,
                start_time=time(14, 30),
                end_time=time(15, 30),
                label="Break B",
            ),
        ],
    )

    with pytest.raises(HTTPException) as exc:
        service.replace_schedule_template(payload)

    assert exc.value.status_code == 409


def test_create_date_block_success():
    service = build_service()
    service.replace_schedule_template(valid_template())

    result = service.create_date_block(
        DateBlockCreate(
            block_date=date(2026, 3, 16),  # Monday
            start_time=time(16, 0),
            end_time=time(17, 0),
            reason="Manual block",
        )
    )

    assert result.reason == "Manual block"


def test_create_date_block_rejects_overlap():
    service = build_service()
    service.replace_schedule_template(valid_template())

    service.create_date_block(
        DateBlockCreate(
            block_date=date(2026, 3, 16),
            start_time=time(16, 0),
            end_time=time(17, 0),
            reason="First block",
        )
    )

    with pytest.raises(HTTPException) as exc:
        service.create_date_block(
            DateBlockCreate(
                block_date=date(2026, 3, 16),
                start_time=time(16, 30),
                end_time=time(17, 30),
                reason="Overlapping block",
            )
        )

    assert exc.value.status_code == 409


def test_get_day_schedule_for_non_working_day():
    service = build_service()

    result = service.get_day_schedule(date(2026, 3, 18))

    assert result.is_working_day is False
    assert result.start_time is None
    assert result.end_time is None
    assert result.breaks == []