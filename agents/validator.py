def validate_input(
    disease,
    allergies,
    age=None,
    weight=None,
    height=None,
    deficiencies=None,
    goal=None
):
    """
    Validates and structures user input for the diet planning pipeline.
    """

    # ========================
    # CLEAN BASIC INPUTS
    # ========================
    disease = disease.strip().lower() if disease else "none"

    allergies_list = []
    if allergies:
        allergies_list = [
            a.strip().lower()
            for a in allergies.split(",")
            if a.strip()
        ]

    deficiencies_list = []
    if deficiencies:
        deficiencies_list = [
            d.strip().lower()
            for d in deficiencies.split(",")
            if d.strip()
        ]

    # ========================
    # NUMERIC VALIDATION
    # ========================
    try:
        age = int(age) if age else None
    except:
        age = None

    try:
        weight = float(weight) if weight else None
    except:
        weight = None

    try:
        height = float(height) if height else None
    except:
        height = None

    # ========================
    # BMI CALCULATION
    # ========================
    bmi = None
    if weight and height:
        height_m = height / 100
        if height_m > 0:
            bmi = round(weight / (height_m ** 2), 2)

    # ========================
    # DEFAULT VALUES
    # ========================
    if not goal:
        goal = "maintenance"

    goal = goal.lower().strip()

    # ========================
    # FINAL STRUCTURED OUTPUT
    # ========================
    user_data = {
        "disease": disease,
        "allergies": allergies_list,
        "deficiencies": deficiencies_list,
        "age": age,
        "weight": weight,
        "height": height,
        "bmi": bmi,
        "goal": goal
    }

    return user_data