from app.shipping.schemas import ShippingRateRequest, ShippingRateResponse, ShippingRateOption


class ShippingProviderClient:
    """
    Cliente abstracto para proveedores de envío.
    Actualmente usa simulación.
    """

    async def get_rates(self, data: ShippingRateRequest) -> ShippingRateResponse:

        weight = data.parcel.weight_kg

        base_bluexpress = 4990
        base_chilexpress = 3990

        extra = 0
        if weight > 1:
            extra = int((weight - 1) * 1200)

        options = [
            ShippingRateOption(provider="Bluexpress", service="Express", price=base_bluexpress + extra),
            ShippingRateOption(provider="Chilexpress", service="Standard", price=base_chilexpress + extra),
        ]

        selected = min(options, key=lambda x: x.price)

        return ShippingRateResponse(options=options, selected=selected)
    