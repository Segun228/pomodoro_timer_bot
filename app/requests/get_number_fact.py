import aiohttp
import logging

NUMBERS_API_URL = "http://numbersapi.com/random/math"

async def get_random_number_fact_async():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(NUMBERS_API_URL) as response:
                response.raise_for_status()
                fact_text = await response.text()
                return fact_text
        except aiohttp.ClientError as e:
            logging.error(f"Ошибка при запросе к Numbers API: {e}")
            return None