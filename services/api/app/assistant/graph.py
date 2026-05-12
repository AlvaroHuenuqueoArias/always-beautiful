from app.assistant.prompts import build_prompt_messages
from app.assistant.policies import get_booking_conversion_flow_step
from app.assistant.state import AssistantFlowStep, AssistantIntent, AssistantState
from app.assistant.tools.booking_tools import build_booking_guidance
from app.assistant.tools.catalog_tools import build_product_guidance
from app.assistant.tools.cart_tools import build_cart_next_actions
from app.assistant.tools.payment_tools import get_booking_deposit_policy

try:
    from langgraph.graph import END, StateGraph
except ImportError:
    END = None
    StateGraph = None


BOOKING_ACTION_KEYWORDS = {
    "agenda",
    "agendar",
    "cita",
    "hora",
    "reservar",
    "reserva",
}

BOOKING_SERVICE_KEYWORDS = {
    "servicio",
    "tratamiento",
    "peinado",
    "corte",
    "facial",
    "estilismo",
}

PRODUCT_KEYWORDS = {
    "comprar",
    "compra",
    "producto",
    "carrito",
    "shampoo",
    "crema",
    "serum",
    "mascarilla",
    "recomienda",
    "recomendación",
}


def classify_intent_node(state: AssistantState) -> AssistantState:
    normalized_message = state["message"].lower()
    prompt_messages = build_prompt_messages(state["message"])
    has_booking_action = any(
        keyword in normalized_message
        for keyword in BOOKING_ACTION_KEYWORDS
    )
    has_booking_service = any(
        keyword in normalized_message
        for keyword in BOOKING_SERVICE_KEYWORDS
    )
    has_product_signal = any(
        keyword in normalized_message for keyword in PRODUCT_KEYWORDS
    )

    if has_booking_action:
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
    guidance = build_booking_guidance(state["message"])
    deposit_policy = get_booking_deposit_policy()

    return {
        **state,
        "flow_step": get_booking_conversion_flow_step(state["message"]),
        "response_message": str(guidance["message"]),
        "requires_deposit": bool(deposit_policy["requires_deposit"]),
        "deposit_percentage": int(deposit_policy["deposit_percentage"]),
        "next_actions": list(guidance["next_actions"]),
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
    }


def general_node(state: AssistantState) -> AssistantState:
    return {
        **state,
        "flow_step": AssistantFlowStep.COMPLETED.value,
        "response_message": (
            "Puedo ayudarte a iniciar una reserva de servicio o tratamiento, "
            "o a orientar una compra de productos desde la web."
        ),
        "requires_deposit": False,
        "deposit_percentage": 0,
        "next_actions": [
            "Indicar si deseas reservar una hora.",
            "Indicar si buscas una recomendación de producto.",
        ],
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
