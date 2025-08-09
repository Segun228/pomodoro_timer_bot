import aiohttp
import logging

JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any?type=single"

async def get_random_joke_async():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(JOKE_API_URL) as response:
                response.raise_for_status()
                
                data = await response.json()

                if "joke" in data:
                    return data["joke"]
                else:
                    return None
        except aiohttp.ClientError as e:
            logging.error(f"Ошибка при запросе к JokeAPI: {e}")
            return None