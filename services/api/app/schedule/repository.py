from datetime import date
from typing import Dict, List, Optional
from uuid import UUID

from app.schedule.schemas import (
    DateBlockResponse,
    DailyBreak,
    ScheduleTemplateResponse,
    WeeklyScheduleRule,
)


class ScheduleRepository:
    def __init__(self) -> None:
        self._weekly_rules: List[WeeklyScheduleRule] = []
        self._breaks: List[DailyBreak] = []
        self._date_blocks: Dict[UUID, DateBlockResponse] = {}

    def reset(self) -> None:
        self._weekly_rules = []
        self._breaks = []
        self._date_blocks = {}

    def get_template(self) -> ScheduleTemplateResponse:
        return ScheduleTemplateResponse(
            weekly_rules=list(self._weekly_rules),
            breaks=list(self._breaks),
        )

    def replace_template(
        self,
        weekly_rules: List[WeeklyScheduleRule],
        breaks: List[DailyBreak],
    ) -> ScheduleTemplateResponse:
        self._weekly_rules = list(weekly_rules)
        self._breaks = list(breaks)

        return ScheduleTemplateResponse(
            weekly_rules=list(self._weekly_rules),
            breaks=list(self._breaks),
        )

    def list_blocks(self) -> List[DateBlockResponse]:
        return list(self._date_blocks.values())

    def add_block(self, block: DateBlockResponse) -> DateBlockResponse:
        self._date_blocks[block.id] = block
        return block

    def delete_block(self, block_id: UUID) -> bool:
        if block_id not in self._date_blocks:
            return False

        del self._date_blocks[block_id]
        return True

    def get_block_by_id(self, block_id: UUID) -> Optional[DateBlockResponse]:
        return self._date_blocks.get(block_id)

    def get_blocks_for_date(self, target_date: date) -> List[DateBlockResponse]:
        result: List[DateBlockResponse] = []

        for block in self._date_blocks.values():
            if block.block_date == target_date:
                result.append(block)

        return result

    def get_rule_for_day(self, day_of_week: int) -> Optional[WeeklyScheduleRule]:
        for rule in self._weekly_rules:
            if rule.day_of_week == day_of_week:
                return rule
        return None

    def get_breaks_for_day(self, day_of_week: int) -> List[DailyBreak]:
        result: List[DailyBreak] = []

        for item in self._breaks:
            if item.day_of_week == day_of_week:
                result.append(item)

        return result