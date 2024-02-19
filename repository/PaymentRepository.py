from util import Database, RedisSession
from typing import Tuple, Union
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
    
    def get_payment_status(self, payment_id: str) -> Union[str, dict]:
        query = "SELECT * FROM payments WHERE payment_id = %s"
        success, err = self.db_session.execute_query(query, (payment_id,))
        if not success:
            return success, str(err)
        data = self.db_session.get_cursor().fetchone()
        return success, data


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
            sql_query = "UPDATE bookings SET status = %s, updated_at = %s, is_paid = true WHERE payment_id = %s RETURNING id"
            payment_query = ("INSERT INTO payments (booking_id, amount, currency, status, payment_intent_id) VALUES  ("
                             "%s, %s, %s, %s, %s)")
            success, err = self.db_session.execute_query(sql_query, ("confirmed", datetime.now(), payment_intent.id))
            if not success:
                self.db_session.rollback()
                return False, err

            success, err = self.db_session.execute_query(payment_query, (
                payment_intent.metadata.booking_id,
                payment_intent.amount,
                payment_intent.currency,
                payment_intent.status,
                payment_intent.id
            ))
            if not success:
                self.db_session.rollback()
                return False, err
            # TODO: Mark Stay as booked for the period
            stay_query = "UPDATE stays SET is_available = false, booked_by = %s, booked_until = %s, updated_at = %s WHERE id = %s"
            success, err = self.db_session.execute_query(stay_query, (
                payment_intent.metadata.user_id,
                payment_intent.metadata.checkout_date,
                datetime.now().strftime("%Y-%m-%d"),
                payment_intent.metadata.stay_id
            ))
            if not success:
                self.db_session.rollback()
                return False, err
            print(f"PaymentIntent was successful: {payment_intent.id}")
        elif event_dict['type'] == 'payment_intent.payment_failed':
            payment_intent = event_dict['data']['object']
            print(f"PaymentIntent failed: {payment_intent.id}")
            return False, "PaymentIntent failed"
        self.db_session.commit()
        return True, "OK"
