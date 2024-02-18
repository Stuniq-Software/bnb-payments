from util import Database, RedisSession
from typing import Tuple
from datetime import datetime
import stripe
import os

stripe.api_key = os.getenv("STRIPE_API_KEY")


class PaymentRepository:
    db_session: Database
    redis_session: RedisSession

    def __init__(self, db_session: Database, redis_session: RedisSession):
        self.db_session = db_session
        self.redis_session = redis_session

    def get_intent(self, payment_id: str) -> str:
        intent = stripe.PaymentIntent.retrieve(payment_id)
        return intent.client_secret

    def webhook_handler(self, payload, sig_header, event) -> Tuple[bool, str]:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, os.getenv("STRIPE_ENDPOINT_SECRET")
            )
        except ValueError as e:
            return False, str(e)

        except stripe.error.SignatureVerificationError as e:
            return False, str(e)

        event_dict = event.to_dict()
        if event_dict['type'] == 'payment_intent.succeeded':
            payment_intent = event_dict['data']['object']
            sql_query = "UPDATE bookings SET payment_status = %s, updated_at = %s WHERE payment_id = %s RETURNING id"
            payment_query = ("INSERT INTO payments (booking_id, amount, currency, status, payment_intent_id) VALUES  ("
                             "%s, %s, %s, %s, %s)")
            success, err = self.db_session.execute_query(sql_query, ("paid", datetime.now(), payment_intent.id))
            if not success:
                return False, err

            success, err = self.db_session.execute_query(payment_query, (
                payment_intent.metadata.booking_id,
                payment_intent.amount,
                payment_intent.currency,
                payment_intent.status,
                payment_intent.id
            ))
            if not success:
                return False, err
            print(f"PaymentIntent was successful: {payment_intent.id}")
        elif event_dict['type'] == 'payment_intent.payment_failed':
            payment_intent = event_dict['data']['object']
            print(f"PaymentIntent failed: {payment_intent.id}")
            return False, "PaymentIntent failed"
        return True, "OK"
