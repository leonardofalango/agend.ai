from database.get_instance import get_instance
from logger import logger


async def get_company(phone_number_id) -> dict:
    """
    Middleware function to extract tenant ID from the request headers.
    Assumes that the tenant ID is passed in the 'X-Tenant-ID' header.
    """
    try:
        logger.debug("Retrieving company")
        res = (
            get_instance()
            .table("company")
            .select("*")
            .eq("phone_number", phone_number_id)
            .single()
            .execute()
        )

        logger.debug(f"Database response: {res}")

        if not res.data:
            logger.error("Company not found")
            raise ValueError("Company not found")

        return res.data
    except Exception as e:
        logger.error(f"Error retrieving company: {e}")
        raise e
