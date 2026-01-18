from dotenv import load_dotenv

load_dotenv()
import asyncio

# from llm.process_message import process_ai_message
from middlewares.tenant import get_company
from logger import logger

logger.info("testing")

asyncio.run(get_company("41987141533"))

# asyncio.run(process_ai_message(user_message="Qual a cor do céu?", company=company))
