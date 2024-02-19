from typing import List, Optional


class Payment:
    id: str
    booking_id: str
    amount: float
    currency: str
    status: str
    payment_intent_id: str
    created_at: Optional[str]
    updated_at: Optional[str]

    def __init__(self):
        self.id = ""
        self.booking_id = ""
        self.amount = 0.0
        self.currency = ""
        self.status = ""
        self.created_at = None
        self.updated_at = None

    @staticmethod
    def from_tuple(payment_tuple: tuple):
        payment = Payment()
        payment.id = payment_tuple[0]
        payment.booking_id = payment_tuple[1]
        payment.amount = payment_tuple[2] / 100
        payment.currency = payment_tuple[3]
        payment.status = payment_tuple[4]
        payment.created_at = payment_tuple[6]
        payment.updated_at = payment_tuple[7]
        return payment

    def to_dict(self):
        return {
            "id": self.id,
            "booking_id": self.booking_id,
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
