import aiohttp
import logging

DOG_API_URL = "https://api.thedogapi.com/v1/images/search?mime_types=gif"

async def get_random_dog_gif_async():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(DOG_API_URL) as response:
                response.raise_for_status()
                

                data = await response.json()

                if data and data[0] and "url" in data[0]:
                    return data[0]["url"]
                else:
                    return None
        except aiohttp.ClientError as e:
            logging.error(f"Ошибка при запросе к API: {e}")
            return None