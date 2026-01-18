from llm.get_model import get_model
from logger import logger
from tools import google_sheets_agent


async def process_ai_message(
    user_message: str, company: dict, chat_history: list = None
):
    """
    Process incoming AI message requests.
    """
    logger.debug(f"Processing AI message from company: {company.get('id')}")

    prompt_base = company.get("prompt", None)
    if not prompt_base:
        logger.error("Prompt not found")
        raise ValueError("Prompt not found in company data")

    model = get_model()
    chat = model.start_chat(history=chat_history or [])

    spreadsheet_id = company.get("spreadsheet_id")
    range_name = company.get("range_name", None)
    rows = await google_sheets_agent.read_google_sheet(
        spreadsheet_id=spreadsheet_id,
    )
    availability_context = await google_sheets_agent.format_sheets_llm(rows)

    try:
        full_user_input = (
            f"Context: {prompt_base}\n\n"
            f"Availible datetimes for appointments: {availability_context}\n\n"
            f"User message: {user_message}\n\n"
        )

        response = chat.send_message(full_user_input)
        tool_call = response.candidates[0].content.parts[0].function_call
        if tool_call:
            logger.debug(f"Tool called: {tool_call.name}, tools args {tool_call.args}")
            if tool_call.name == "confirm_appointment":
                called_successfully = (
                    await google_sheets_agent.update_appointment_in_sheet(
                        spreadsheet_id=tool_call.args["spreadsheet_id"],
                        row_index=tool_call.args["row_index"],
                        client_name=tool_call.args["client_name"],
                    )
                )

                if called_successfully:
                    response = chat.send_message(
                        "The appointment has been successfully booked."
                    )
                else:
                    response = chat.send_message(
                        "There was an error booking the appointment. Please try again later."
                    )

        usage_metadata = response.usage_metadata
        logger.debug(
            f"Tokens: {usage_metadata.prompt_token_count}, Resposta: {usage_metadata.candidates_token_count}"
        )

        logger.debug(f"Response from Gemini: {response.text}")

        return {"text": response.text, "tokens": usage_metadata.total_token_count}

    except Exception as e:
        logger.error(f"error calling gemini {str(e)}")
        return {
            "text": "Desculpe, tive um problema técnico. Pode repetir?",
            "tokens": 0,
        }
