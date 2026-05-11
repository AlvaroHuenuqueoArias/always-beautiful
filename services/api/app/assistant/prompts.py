ASSISTANT_SYSTEM_PROMPT = """
Eres el asistente comercial de Always Beautiful.
Tu rol es orientar a clientas hacia reservas de servicios o tratamientos y
hacia compra o recomendacion de productos desde la web.
No confirmas horarios reales, precios reales, disponibilidad real ni pagos
reales. Para reservas, siempre informas que la confirmacion requiere cancelar
el 20% del valor del servicio desde la web.
""".strip()


def build_prompt_messages(user_message: str):
    try:
        from langchain_core.messages import HumanMessage, SystemMessage
    except ImportError:
        return [
            {"role": "system", "content": ASSISTANT_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]

    return [
        SystemMessage(content=ASSISTANT_SYSTEM_PROMPT),
        HumanMessage(content=user_message),
    ]
