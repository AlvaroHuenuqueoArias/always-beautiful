from pydantic import BaseModel
from typing import Optional


class PaymentIntent(BaseModel):
    order_id: str
    amount: float
    currency: str = "CLP"


class PaymentStatus(BaseModel):
    payment_id: str
    status: str


class WebhookEvent(BaseModel):
    event_id: str
    type: str
    data: Optional[dict] = None