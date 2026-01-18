import os
import httpx

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")


async def send_whatsapp_message(to_number: str, message: str, phone_id: str):
    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message},
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=data, headers=headers)
