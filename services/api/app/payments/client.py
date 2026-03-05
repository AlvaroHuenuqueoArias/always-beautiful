class PaymentProviderClient:

    def create_payment(self, order_id: str, amount: float):

        return {
            "payment_id": "simulated_payment_123",
            "status": "created",
            "order_id": order_id,
            "amount": amount
        }