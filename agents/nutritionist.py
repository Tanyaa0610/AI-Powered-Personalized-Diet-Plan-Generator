import math
import os

# OPTIONAL GEMINI
try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    GEMINI = True
except:
    GEMINI = False


def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return round(weight / (height_m ** 2), 2)


def generate_diet(data, user):

    age = user["age"]
    weight = user["weight"]
    height = user["height"]
    goal = user["goal"]
    deficiencies = user["deficiencies"]

    bmi = calculate_bmi(weight, height)

    # -------------------------------
    # CALORIES
    # -------------------------------
    calories = int(25 * weight)

    if goal == "weight loss":
        calories -= 300
    elif goal == "muscle gain":
        calories += 300

    # -------------------------------
    # BASE MEALS
    # -------------------------------
    meals = data.get("meals", {})

    if not meals:
        meals = {
            "breakfast": ["Oats + fruits", "Smoothie", "Eggs + toast"],
            "lunch": ["Rice + dal", "Chapati + sabzi", "Quinoa bowl"],
            "dinner": ["Soup + salad", "Paneer + roti", "Grilled vegetables"],
            "snacks": ["Fruits", "Nuts", "Roasted chickpeas"]
        }

    # -------------------------------
    # BMI LOGIC
    # -------------------------------
    if bmi > 25:
        meals["snacks"] = ["Low calorie fruits", "Salad", "Green tea snacks"]

    elif bmi < 18.5:
        meals["snacks"] = ["Peanut butter toast", "Milk shake", "Dry fruits"]

    # -------------------------------
    # DEFICIENCY LOGIC
    # -------------------------------
    extra_foods = []

    for d in deficiencies:
        if "iron" in d:
            extra_foods += ["spinach", "beetroot"]
        if "vitamin d" in d:
            extra_foods += ["mushrooms", "egg yolk"]
        if "b12" in d:
            extra_foods += ["eggs", "fish"]

    eat = list(set(data.get("eat", []) + extra_foods))

    # -------------------------------
    # GEMINI (AI GENERATION)
    # -------------------------------
    if GEMINI:
        try:
            model = genai.GenerativeModel("gemini-pro")

            prompt = f"""
            Generate a personalized diet plan.
            Disease: {user['disease']}
            Age: {age}
            BMI: {bmi}
            Goal: {goal}
            Deficiencies: {deficiencies}
            """

            response = model.generate_content(prompt)

            return {
                "eat": eat,
                "avoid": data.get("avoid", []),
                "meals": meals,
                "tips": [response.text[:300]]
            }

        except:
            pass

    return {
        "eat": eat,
        "avoid": data.get("avoid", []),
        "meals": meals,
        "calories": calories,
        "bmi": bmi,
        "tips": [
            f"BMI: {bmi}",
            f"Daily Calories: {calories}",
            f"Goal: {goal}"
        ]
    }