import requests
import os


def generate_recipes():

    try:
        API_KEY = os.getenv("SPOON_API_KEY")

        url = "https://api.spoonacular.com/recipes/random"

        params = {
            "number": 1,
            "apiKey": API_KEY
        }

        res = requests.get(url, params=params, timeout=5)

        if res.status_code == 200:
            data = res.json()

            recipe = data.get("recipes", [])[0]

            return {
                "breakfast": recipe.get("title", "Healthy meal")
            }

    except Exception as e:
        print("⚠️ Recipe API failed:", e)

    return {
        "breakfast": "Oats bowl",
        "lunch": "Dal + rice",
        "dinner": "Grilled vegetables"
    }