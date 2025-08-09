import aiohttp
import logging

base_url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"

async def get_cocktail_async():
    """
    Асинхронно получает случайный коктейль из The Cocktail DB API.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(base_url) as response:
                response.raise_for_status()
                data = await response.json()
                
                if data is None:
                    raise ValueError("Не удалось получить данные о коктейле.")
                
                return data
        except aiohttp.ClientError as e:
            logging.error(f"Ошибка при запросе к API коктейлей: {e}")
            return None
        except ValueError as e:
            logging.error(f"Ошибка данных: {e}")
            return None


def get_ingredients_list(cocktail_info: dict) -> str:
    """
    Формирует список ингредиентов и их количество из словаря с данными о коктейле.
    """
    ingredients = []
    for i in range(1, 16):
        ingredient_key = f"strIngredient{i}"
        measure_key = f"strMeasure{i}"

        ingredient = cocktail_info.get(ingredient_key)
        measure = cocktail_info.get(measure_key)
        
        if ingredient and ingredient.strip():
            if measure and measure.strip():
                ingredients.append(f"• {ingredient.strip()} - {measure.strip()}")
            else:
                ingredients.append(f"• {ingredient.strip()}")
    
    return "\n".join(ingredients)