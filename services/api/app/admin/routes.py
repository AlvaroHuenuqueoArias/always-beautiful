from datetime import date

from fastapi import APIRouter, Depends, Query, status

from app.admin.schemas import AdminDashboardResponse, AdminSummaryResponse
from app.admin.service import AdminService
from app.auth.dependencies import require_admin_access
from app.db.models import AdminUser

router = APIRouter(prefix="/admin", tags=["admin"])

admin_service = AdminService()


@router.get(
    "/dashboard",
    response_model=AdminDashboardResponse,
    status_code=status.HTTP_200_OK,
)
def get_dashboard(
    booking_date: date = Query(default_factory=date.today),
    professional_id: str | None = Query(default=None),
    _current_user: AdminUser = Depends(require_admin_access),
) -> AdminDashboardResponse:
    return admin_service.get_dashboard(
        booking_date=booking_date,
        professional_id=professional_id,
    )


@router.get(
    "/summary",
    response_model=AdminSummaryResponse,
    status_code=status.HTTP_200_OK,
)
def get_summary(
    booking_date: date = Query(default_factory=date.today),
    professional_id: str | None = Query(default=None),
    _current_user: AdminUser = Depends(require_admin_access),
) -> AdminSummaryResponse:
    return admin_service.get_summary(
        booking_date=booking_date,
        professional_id=professional_id,
    )