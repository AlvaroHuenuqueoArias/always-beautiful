from fastapi import APIRouter, BackgroundTasks
from .schemas import PaymentIntent, WebhookEvent
from .client import PaymentProviderClient


router = APIRouter(
    prefix="/payments",
    tags=["payments"]
)

client = PaymentProviderClient()

processed_events = set()


@router.post("/create")
def create_payment(intent: PaymentIntent):

    payment = client.create_payment(
        order_id=intent.order_id,
        amount=intent.amount
    )

    return payment


@router.post("/webhook")
def payments_webhook(event: WebhookEvent, background_tasks: BackgroundTasks):

    if event.event_id in processed_events:
        return {"status": "duplicate ignored"}

    processed_events.add(event.event_id)

    background_tasks.add_task(process_event, event)

    return {"status": "received"}


def process_event(event: WebhookEvent):

    print("Processing event:", event.event_id)