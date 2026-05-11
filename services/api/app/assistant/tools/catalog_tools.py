PRODUCT_FOCUS_KEYWORDS = {
    "shampoo": "cuidado capilar",
    "acondicionador": "cuidado capilar",
    "mascarilla": "tratamiento capilar",
    "crema": "cuidado facial",
    "serum": "cuidado facial",
    "producto": "producto",
}


def detect_product_focus(message: str) -> str:
    normalized_message = message.lower()

    for keyword, focus in PRODUCT_FOCUS_KEYWORDS.items():
        if keyword in normalized_message:
            return focus

    return "producto"


def build_product_guidance(message: str) -> dict[str, object]:
    product_focus = detect_product_focus(message)

    return {
        "message": (
            "Puedo orientarte para revisar productos desde la página web. "
            f"Para esta consulta, el foco sugerido es {product_focus}; "
            "la compra debe continuar en el catálogo y carrito web."
        ),
        "next_actions": [
            "Revisar productos activos en la página web.",
            "Comparar descripción y uso recomendado antes de agregar al carrito.",
            "Agregar el producto al carrito desde la web.",
        ],
    }

