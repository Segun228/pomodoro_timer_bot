import aiohttp
import logging
import asyncio

BORED_API_URL = "https://bored-api.appbrewery.com/random"

async def get_random_activity_async():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(BORED_API_URL) as response:
                response.raise_for_status()
                data = await response.json()

                if "activity" in data.keys():
                    return data["activity"]
                else:
                    return None
        except aiohttp.ClientError as e:
            logging.error(f"Ошибка при запросе к API: {e}")
            return None


async def main():
    activity_text = await get_random_activity_async()
    if activity_text:
        print("Вот идея, чем заняться:\n")
        print(activity_text)
    else:
        print("Не удалось получить идею. Попробуйте позже.")


if __name__ == "__main__":
    asyncio.run(main())