from app.assistant.prompts import build_prompt_messages
from app.assistant.policies import (
    SERVICE_CATEGORY_UNKNOWN,
    detect_requested_professional,
    detect_service_category,
    detects_all_services_intent,
    detects_booking_intent,
    detects_product_intent,
    get_booking_conversion_flow_step,
)
from app.assistant.state import AssistantFlowStep, AssistantIntent, AssistantState
from app.assistant.tools.booking_tools import build_booking_guidance
from app.assistant.tools.catalog_tools import build_product_guidance
from app.assistant.tools.cart_tools import (
    build_cart_next_actions,
    detects_deposit_handoff_intent,
)
from app.assistant.tools.payment_tools import get_booking_deposit_policy

try:
    from langgraph.graph import END, StateGraph
except ImportError:
    END = None
    StateGraph = None


def classify_intent_node(state: AssistantState) -> AssistantState:
    prompt_messages = build_prompt_messages(state["message"])
    context = state.get("metadata", {}).get("context", {})
    has_booking_action = detects_booking_intent(state["message"])
    has_booking_service = (
        detect_service_category(state["message"]) != SERVICE_CATEGORY_UNKNOWN
    )
    has_product_signal = detects_product_intent(state["message"])
    has_deposit_handoff = detects_deposit_handoff_intent(state["message"])
    has_professional_signal = detect_requested_professional(state["message"]) is not None
    has_all_services_signal = detects_all_services_intent(state["message"])
    has_booking_context = isinstance(context, dict) and bool(
        context.get("selected_professional")
        or context.get("selected_service")
        or context.get("requested_day")
        or context.get("requested_time")
    )

    if (
        has_booking_action
        or has_deposit_handoff
        or has_professional_signal
        or has_all_services_signal
        or has_booking_context
    ):
        intent = AssistantIntent.BOOKING.value
    elif has_product_signal:
        intent = AssistantIntent.PRODUCT_RECOMMENDATION.value
    elif has_booking_service:
        intent = AssistantIntent.BOOKING.value
    else:
        intent = AssistantIntent.GENERAL.value

    metadata = dict(state.get("metadata", {}))
    metadata["prompt_message_count"] = len(prompt_messages)

    return {
        **state,
        "intent": intent,
        "metadata": metadata,
    }


def booking_node(state: AssistantState) -> AssistantState:
    context = state.get("metadata", {}).get("context", {})
    guidance = build_booking_guidance(state["message"], context)
    deposit_policy = get_booking_deposit_policy()

    return {
        **state,
        "flow_step": guidance.get(
            "flow_step",
            get_booking_conversion_flow_step(state["message"]),
        ),
        "response_message": str(guidance["message"]),
        "requires_deposit": bool(deposit_policy["requires_deposit"]),
        "deposit_percentage": int(deposit_policy["deposit_percentage"]),
        "next_actions": list(guidance["next_actions"]),
        "redirect_target": guidance.get("redirect_target"),
        "cart_payload": guidance.get("cart_payload"),
        "context": guidance.get("context", {}),
        "quick_replies": list(guidance.get("quick_replies", [])),
    }


def product_recommendation_node(state: AssistantState) -> AssistantState:
    guidance = build_product_guidance(state["message"])
    next_actions = list(guidance["next_actions"]) + build_cart_next_actions()

    return {
        **state,
        "flow_step": AssistantFlowStep.PRODUCT_SELECTION.value,
        "response_message": str(guidance["message"]),
        "requires_deposit": False,
        "deposit_percentage": 0,
        "next_actions": next_actions,
        "context": {
            "intent": AssistantIntent.PRODUCT_RECOMMENDATION.value,
            "flow_step": AssistantFlowStep.PRODUCT_SELECTION.value,
        },
        "quick_replies": [
            {
                "label": "Ver productos",
                "message": "Quiero ver productos disponibles para comprar",
                "action_type": "navigate",
                "target": "/products",
                "payload": {"reason": "product_catalog"},
            }
        ],
    }


def general_node(state: AssistantState) -> AssistantState:
    return {
        **state,
        "flow_step": AssistantFlowStep.COMPLETED.value,
        "response_message": (
            "Hola, soy la asistente virtual de Always Beautiful. Puedo "
            "ayudarte a reservar una hora, revisar servicios o ver productos. "
            "¿Qué quieres hacer?"
        ),
        "requires_deposit": False,
        "deposit_percentage": 0,
        "next_actions": [
            "Puedes iniciar una reserva guiada desde el chat.",
            "También puedes pedir orientación de productos.",
        ],
        "quick_replies": [
            {
                "label": "Reservar hora",
                "message": "Quiero reservar una hora",
                "action_type": "reply",
                "target": None,
                "payload": {"reason": "booking_start"},
            },
            {
                "label": "Ver servicios",
                "message": "Quiero ver todos los servicios disponibles",
                "action_type": "navigate",
                "target": "/services",
                "payload": {"reason": "full_services_catalog"},
            },
            {
                "label": "Ver productos",
                "message": "Quiero comprar productos",
                "action_type": "navigate",
                "target": "/products",
                "payload": {"reason": "product_start"},
            },
        ],
        "context": {
            "intent": AssistantIntent.GENERAL.value,
            "flow_step": AssistantFlowStep.COMPLETED.value,
        },
    }


def route_by_intent(state: AssistantState) -> str:
    return state.get("intent", AssistantIntent.GENERAL.value)


def build_langgraph_runner():
    if StateGraph is None or END is None:
        return None

    try:
        workflow = StateGraph(AssistantState)
        workflow.add_node("classify_intent", classify_intent_node)
        workflow.add_node(AssistantIntent.BOOKING.value, booking_node)
        workflow.add_node(
            AssistantIntent.PRODUCT_RECOMMENDATION.value,
            product_recommendation_node,
        )
        workflow.add_node(AssistantIntent.GENERAL.value, general_node)
        workflow.set_entry_point("classify_intent")
        workflow.add_conditional_edges(
            "classify_intent",
            route_by_intent,
            {
                AssistantIntent.BOOKING.value: AssistantIntent.BOOKING.value,
                AssistantIntent.PRODUCT_RECOMMENDATION.value:
                    AssistantIntent.PRODUCT_RECOMMENDATION.value,
                AssistantIntent.GENERAL.value: AssistantIntent.GENERAL.value,
            },
        )
        workflow.add_edge(AssistantIntent.BOOKING.value, END)
        workflow.add_edge(AssistantIntent.PRODUCT_RECOMMENDATION.value, END)
        workflow.add_edge(AssistantIntent.GENERAL.value, END)
        return workflow.compile()
    except Exception:
        return None


class AssistantGraphRunner:
    def __init__(self) -> None:
        self._langgraph_runner = build_langgraph_runner()

    def run(self, state: AssistantState) -> AssistantState:
        if self._langgraph_runner is not None:
            return self._langgraph_runner.invoke(state)

        classified_state = classify_intent_node(state)
        intent = classified_state["intent"]

        if intent == AssistantIntent.BOOKING.value:
            return booking_node(classified_state)

        if intent == AssistantIntent.PRODUCT_RECOMMENDATION.value:
            return product_recommendation_node(classified_state)

        return general_node(classified_state)
