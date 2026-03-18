from datetime import date

from fastapi import APIRouter, Query, status

from app.admin.schemas import AdminDashboardResponse
from app.admin.service import AdminService

router = APIRouter(prefix="/admin", tags=["admin"])

admin_service = AdminService()


@router.get(
    "/dashboard",
    response_model=AdminDashboardResponse,
    status_code=status.HTTP_200_OK,
)
def get_dashboard(
    booking_date: date = Query(default_factory=date.today),
) -> AdminDashboardResponse:
    return admin_service.get_dashboard(booking_date)