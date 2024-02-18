import stripe
import os


stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_payment_id(amount: float, currency: str, description: str) -> str:
    intent = stripe.PaymentIntent.create(
        amount=int(amount*100),
        currency=currency,
        description=description,
        automatic_payment_methods={"enabled": True}
    )
    return intent['id']

