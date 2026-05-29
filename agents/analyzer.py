# agents/analyzer.py

def analyze_nutrition(user):

    weight = user["weight"]
    height = user["height"]
    age = user["age"]
    goal = user["goal"]

    # -------------------------------
    # BMR (Mifflin-St Jeor)
    # -------------------------------
    bmr = 10 * weight + 6.25 * height - 5 * age + 5

    # activity factor (basic)
    calories = bmr * 1.3

    # goal adjustment
    if goal == "weight loss":
        calories -= 400
    elif goal == "muscle gain":
        calories += 400

    calories = int(calories)

    # -------------------------------
    # MACROS
    # -------------------------------
    protein = int(weight * 1.5)
    fat = int(weight * 0.8)
    carbs = int((calories - (protein * 4 + fat * 9)) / 4)

    # -------------------------------
    # MEAL CALORIES SPLIT (REAL)
    # -------------------------------
    meal_split = {
        "breakfast": int(calories * 0.25),
        "lunch": int(calories * 0.35),
        "dinner": int(calories * 0.25),
        "snacks": int(calories * 0.15)
    }

    return {
        "calories": f"{calories} kcal/day",
        "protein": f"{protein} g",
        "carbs": f"{carbs} g",
        "fat": f"{fat} g",
        "meal_split": meal_split
    }