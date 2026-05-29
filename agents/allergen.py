import json

def filter_allergens(diet, allergies):

    try:
        with open("data/allergies.json") as f:
            allergy_map = json.load(f)

        with open("data/replacements.json") as f:
            replacements = json.load(f)

    except:
        return diet  # fail safe

    banned_items = []

    for user_allergy in allergies:
        user_allergy = user_allergy.lower()

        for category, foods in allergy_map.items():

            if user_allergy == category:
                banned_items.extend(foods)

            elif user_allergy in foods:
                banned_items.append(user_allergy)

    banned_items = list(set(banned_items))

    def replace_text(text):
        text_lower = text.lower()

        for bad in banned_items:
            if bad in text_lower:
                replacement = replacements.get(bad, "safe alternative")
                text = text.replace(bad, replacement)

        return text

    # FILTER EAT
    diet["eat"] = [
        f for f in diet["eat"]
        if not any(b in f.lower() for b in banned_items)
    ]

    # HANDLE MEALS
    meals = diet.get("meals", {})

    if isinstance(meals, dict):
        for meal_type, options in meals.items():

            safe_options = []

            for opt in options:
                new_opt = replace_text(opt)

                if not any(b in new_opt.lower() for b in banned_items):
                    safe_options.append(new_opt)

            if not safe_options:
                safe_options = ["Custom safe meal required"]

            meals[meal_type] = safe_options

    diet["meals"] = meals
    diet["removed_items"] = banned_items

    return diet