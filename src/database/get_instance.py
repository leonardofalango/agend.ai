from supabase import create_client, Client, ClientOptions
from logger import logger

_supabase_client: Client | None = None


def get_instance() -> Client:
    """
    Initializes and returns a Supabase client instance using environment variables.
    """
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    import os

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY must be set in environment variables."
        )

    return create_client(
        supabase_url,
        supabase_key,
        options=ClientOptions(schema="public"),
    )
