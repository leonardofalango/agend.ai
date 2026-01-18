tools = [
    {
        "functionDeclarations": [
            {
                "name": "confirm_appointment",
                "description": "Confirms an appointment for a client at a specified time slot in the Google Sheet.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "spreadsheet_id": {
                            "type": "string",
                            "description": "The ID of the Google Sheet where the appointment is to be booked.",
                        },
                        "row_index": {
                            "type": "integer",
                            "description": "The row index in the Google Sheet that corresponds to the time slot to be booked. Starts with 1 for the first row.",
                        },
                        "client_name": {
                            "type": "string",
                            "description": "The name of the client for whom the appointment is being booked.",
                        },
                    },
                    "required": ["spreadsheet_id", "row_index", "client_name"],
                },
            }
        ]
    }
]
