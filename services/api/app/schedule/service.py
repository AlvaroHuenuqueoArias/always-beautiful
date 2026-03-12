from datetime import date, time
from typing import List
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from app.schedule.repository import ScheduleRepository
from app.schedule.schemas import (
    DateBlockCreate,
    DateBlockResponse,
    DayScheduleResponse,
    DailyBreak,
    ScheduleTemplateResponse,
    ScheduleTemplateUpdate,
    WeeklyScheduleRule,
)


class ScheduleService:
    def __init__(self, repository: ScheduleRepository) -> None:
        self.repository = repository

    def get_schedule_template(self) -> ScheduleTemplateResponse:
        return self.repository.get_template()

    def replace_schedule_template(
        self,
        payload: ScheduleTemplateUpdate,
    ) -> ScheduleTemplateResponse:
        self._validate_weekly_rules_uniqueness(payload.weekly_rules)
        self._validate_breaks_against_rules(
            payload.weekly_rules,
            payload.breaks,
        )

        return self.repository.replace_template(
            weekly_rules=payload.weekly_rules,
            breaks=payload.breaks,
        )

    def list_date_blocks(self) -> List[DateBlockResponse]:
        return self.repository.list_blocks()

    def create_date_block(self, payload: DateBlockCreate) -> DateBlockResponse:
        day_of_week = payload.block_date.weekday()
        rule = self.repository.get_rule_for_day(day_of_week)

        if rule is None or not rule.is_working_day:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Cannot create a date block for a day without a working "
                    "schedule"
                ),
            )

        if rule.start_time is None or rule.end_time is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Working day rule is incomplete",
            )

        if payload.start_time < rule.start_time or payload.end_time > rule.end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Date block must stay within the configured work window",
            )

        existing_blocks = self.repository.get_blocks_for_date(payload.block_date)

        for existing_block in existing_blocks:
            if self._has_overlap(
                payload.start_time,
                payload.end_time,
                existing_block.start_time,
                existing_block.end_time,
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Date block overlaps with an existing block",
                )

        block = DateBlockResponse(
            id=uuid4(),
            block_date=payload.block_date,
            start_time=payload.start_time,
            end_time=payload.end_time,
            reason=payload.reason,
        )

        return self.repository.add_block(block)

    def delete_date_block(self, block_id: UUID) -> None:
        deleted = self.repository.delete_block(block_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Date block not found",
            )

    def get_day_schedule(self, target_date: date) -> DayScheduleResponse:
        day_of_week = target_date.weekday()
        rule = self.repository.get_rule_for_day(day_of_week)
        date_blocks = self.repository.get_blocks_for_date(target_date)

        if rule is None:
            return DayScheduleResponse(
                target_date=target_date,
                day_of_week=day_of_week,
                is_working_day=False,
                start_time=None,
                end_time=None,
                breaks=[],
                date_blocks=date_blocks,
            )

        if not rule.is_working_day:
            return DayScheduleResponse(
                target_date=target_date,
                day_of_week=day_of_week,
                is_working_day=False,
                start_time=None,
                end_time=None,
                breaks=[],
                date_blocks=date_blocks,
            )

        breaks = self.repository.get_breaks_for_day(day_of_week)

        return DayScheduleResponse(
            target_date=target_date,
            day_of_week=day_of_week,
            is_working_day=True,
            start_time=rule.start_time,
            end_time=rule.end_time,
            breaks=breaks,
            date_blocks=date_blocks,
        )

    def _validate_weekly_rules_uniqueness(
        self,
        weekly_rules: List[WeeklyScheduleRule],
    ) -> None:
        seen_days = set()

        for rule in weekly_rules:
            if rule.day_of_week in seen_days:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Duplicate weekly rule detected for "
                        f"day_of_week={rule.day_of_week}"
                    ),
                )

            seen_days.add(rule.day_of_week)

    def _validate_breaks_against_rules(
        self,
        weekly_rules: List[WeeklyScheduleRule],
        breaks: List[DailyBreak],
    ) -> None:
        rules_by_day = {rule.day_of_week: rule for rule in weekly_rules}
        breaks_by_day: dict[int, List[DailyBreak]] = {}

        for item in breaks:
            rule = rules_by_day.get(item.day_of_week)

            if rule is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Break defined for day_of_week={item.day_of_week} "
                        "without a weekly rule"
                    ),
                )

            if not rule.is_working_day:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Break defined for non-working day "
                        f"day_of_week={item.day_of_week}"
                    ),
                )

            if rule.start_time is None or rule.end_time is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Working rule for day_of_week={item.day_of_week} "
                        "is incomplete"
                    ),
                )

            if item.start_time < rule.start_time or item.end_time > rule.end_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Break '{item.label}' is outside the configured work "
                        f"window for day_of_week={item.day_of_week}"
                    ),
                )

            current_day_breaks = breaks_by_day.setdefault(item.day_of_week, [])

            for existing_break in current_day_breaks:
                if self._has_overlap(
                    item.start_time,
                    item.end_time,
                    existing_break.start_time,
                    existing_break.end_time,
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=(
                            f"Break '{item.label}' overlaps another break on "
                            f"day_of_week={item.day_of_week}"
                        ),
                    )

            current_day_breaks.append(item)

    @staticmethod
    def _has_overlap(
        start_a: time,
        end_a: time,
        start_b: time,
        end_b: time,
    ) -> bool:
        return start_a < end_b and end_a > start_b