from fastapi import APIRouter, Response, Request
from dtypes import APIResponse, HttpStatus
from repository import PaymentRepository
from util import Database, RedisSession
import json

payment_service = PaymentRepository(
    db_session=Database(),
    redis_session=RedisSession()
)

router = APIRouter(prefix="/api/v1/payments", tags=["Payment"])


@router.post("/webhook")
async def webhook_route(request: Request, response: Response):
    payload = await request.body()
    event = None

    try:
        event = json.loads(payload)
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        api_resp = APIResponse(status=HttpStatus.INTERNAL_SERVER_ERROR, message="Error decoding JSON", data=None)
        response.status_code = api_resp.status.value
        return api_resp.to_dict()

    sig_header = request.headers.get("stripe-signature")
    success, message = payment_service.webhook_handler(payload, sig_header, event)
    if not success:
        api_resp = APIResponse(status=HttpStatus.INTERNAL_SERVER_ERROR, message=message, data=None)
        response.status_code = api_resp.status.value
        return api_resp.to_dict()

    api_resp = APIResponse(status=HttpStatus.OK, message=message, data=None)
    response.status_code = api_resp.status.value
    return api_resp.to_dict()


@router.get("/{payment_id}")
async def get_payment_intent(payment_id: str, response: Response):
    client_secret = payment_service.get_intent(payment_id)
    api_resp = APIResponse(status=HttpStatus.OK, message="Payment Intent retrieved", data={"client_secret": client_secret})
    response.status_code = api_resp.status.value
    return api_resp.to_dict()
