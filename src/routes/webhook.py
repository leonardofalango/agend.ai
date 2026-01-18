from fastapi import Request, APIRouter

from logger import logger
from llm.process_message import process_ai_message
from middlewares.tenant import get_company
from whatsapp.send_message import send_whatsapp_message
from database.log_message import log_whatsapp_message

webhook_router = APIRouter()


@webhook_router.get("/webhook")
async def verify_webhook(request: Request):
    """
    Verify webhook, for meta
    """
    logger.debug("Verifying webhook")
    params = request.query_params
    return int(params.get("hub.challenge"))


@webhook_router.post("/webhook")
async def handle_message(request: Request):
    """
    Handle incoming messages
    """
    try:
        logger.debug("Handling incoming messages")
        body = await request.json()

        value = body["entry"][0]["changes"][0]["value"]
        if "messages" in value:
            message_data = value["messages"][0]
            whatsapp_uid = message_data["from"]
            text_body = message_data["text"]["body"]
            phone_id = value["metadata"]["phone_number_id"]

            company = await get_company(phone_number_id=phone_id)

            ai_response = await process_ai_message(
                user_message=value["messages"][0], company=company
            )

            await log_whatsapp_message(
                company_id=company["id"],
                message_type="incoming",
                whatsapp_uid=whatsapp_uid,
                input_tokens=len(text_body.split()),
                output_tokens=len(ai_response.split()),
            )

            await send_whatsapp_message(
                to_number=whatsapp_uid, message=ai_response, phone_id=phone_id
            )

        return {"status": "success"}

    except Exception as e:
        logger.error(f"Error handling message: {e}")
        return {"status": "error", "message": "error handliong message"}
