from fastapi import APIRouter
from app.shipping.schemas import ShippingRateRequest, ShippingRateResponse
from app.shipping.client import ShippingProviderClient

router = APIRouter(prefix="/shipping", tags=["shipping"])

client = ShippingProviderClient()

@router.post("/rates", response_model=ShippingRateResponse)
async def get_shipping_rates(data: ShippingRateRequest):
    return await client.get_rates(data)