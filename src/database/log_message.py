from database.get_instance import get_instance
from logger import logger


async def log_whatsapp_message(
    company_id: str,
    message_type: str,
    whatsapp_uid: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
):
    """
    Logs a WhatsApp message to the database.
    """
    try:
        logger.debug("Logging WhatsApp message")
        res = (
            get_instance()
            .table("interation")
            .insert(
                {
                    "company_id": company_id,
                    "message_type": message_type,
                    "whatsapp_uid": whatsapp_uid,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                }
            )
            .execute()
        )

        logger.debug(f"Database response: {res}")

        if res.get("error"):
            logger.error(f"Error logging message: {res['error']}")
            raise ValueError("Error logging message")

        return res.data
    except Exception as e:
        logger.error(f"Exception logging message: {e}")
        raise e
