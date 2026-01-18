import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from logger import logger

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS", "service_account.json"
)


def get_sheets_service():
    """Google Sheets service Singleton"""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    logger.debug("Google Sheets service created")
    return build("sheets", "v4", credentials=creds)


async def read_google_sheet(spreadsheet_id: str, range_name: str = "A:B"):
    """
    Reads data from a Google Sheet.
    * Args:
        spreadsheet_id (str): The ID of the spreadsheet to read from.
        range_name (str): The range of cells to read (default is "A:B").
    """
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(
                spreadsheetId=spreadsheet_id,
                range=range_name,
            )
            .execute()
        )
        values = result.get("values", [])
        logger.debug(f"Read {len(values)} rows")
        if not values:
            logger.warning(f"Not found data in spreadsheet {spreadsheet_id}")
            return []
        return values

    except Exception as e:
        logger.error(f"Error reading Google Sheet: {str(e)}")
        return None


async def format_sheets_llm(rows: list):
    """
    Formats rows from Google Sheets into a prompt for LLM.
    * Args:
        rows (list): List of rows from Google Sheets.
    """

    if not rows:
        return "No data available."

    context_data = "Here is the data from the Google Sheet:\n\n"
    for i, row in enumerate(rows):
        horario = row[0] if len(row) > 0 else "N/A"
        status = "AVAILIBLE" if len(row) < 2 or not row[1] else f"BOOKED"

        context_data += f"{i + 1}. Time: {horario} - Status: {status}\n"

    context_data += "\nPlease use this information to assist with scheduling. Only suggest available time slots."
    logger.debug(f"Formatted for llm {context_data}")
    return context_data


async def update_appointment_in_sheet(
    spreadsheet_id: str, row_index: int, client_name: str
):
    """
    Updates a specific row in the Google Sheet to mark an appointment as booked.
    """
    try:
        service = get_sheets_service()
        range_to_update = f"B{row_index}"

        body = {"values": [[client_name]]}
        service.spreadsheets().values().update(
            spreadsheet_id=spreadsheet_id,
            range=range_to_update,
            valueInputOption="RAW",
            body=body,
        ).execute()
        logger.info(f"{client_name} BOOKED {row_index}")
        return True
    except Exception as e:
        logger.error(f"Error updating Google Sheet: {str(e)}")
        return False
