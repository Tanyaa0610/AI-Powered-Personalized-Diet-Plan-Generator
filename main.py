from agents.validator import validate_input
from agents.researcher import get_research
from agents.nutritionist import generate_diet
from agents.analyzer import analyze_nutrition
from agents.recipe import generate_recipes
from agents.allergen import filter_allergens
from agents.aggregator import aggregate
from agents.json_validator import validate_json
from agents.file_generator import save_files


def main():
    print("\n=== 🥗 AI DIET PLAN GENERATOR ===\n")

    # -------------------------------
    # USER INPUT
    # -------------------------------
    disease = input("Enter disease: ").strip()
    allergies = input("Enter allergies (comma separated): ").strip()

    age = int(input("Enter age: "))
    weight = float(input("Enter weight (kg): "))
    height = float(input("Enter height (cm): "))

    goal = input("Goal (weight loss / muscle gain / maintenance): ").lower()

    deficiencies = input("Deficiencies (comma separated): ").lower().split(",")
    deficiencies = [d.strip() for d in deficiencies if d]

    user = validate_input(disease, allergies)

    user.update({
        "age": age,
        "weight": weight,
        "height": height,
        "goal": goal,
        "deficiencies": deficiencies
    })

    # -------------------------------
    # RESEARCH
    # -------------------------------
    print("\n🔍 Fetching research...")
    research = get_research(user["disease"])

    if not research:
        print("❌ Disease not found")
        return

    # -------------------------------
    # DIET
    # -------------------------------
    diet = generate_diet(research, user)

    # -------------------------------
    # NUTRITION + RECIPES
    # -------------------------------
    nutrition = analyze_nutrition(user)
    recipes = generate_recipes()

    # -------------------------------
    # ALLERGEN FILTER
    # -------------------------------
    diet = filter_allergens(diet, user["allergies"])

    # -------------------------------
    # FINAL OUTPUT
    # -------------------------------
    final = aggregate(
        user["disease"],
        diet,
        nutrition,
        recipes
    )

    if not validate_json(final):
        print("❌ Invalid JSON")
        return

    json_file, pdf_file = save_files(final)

    print("\n✅ DONE")
    print("JSON:", json_file)
    print("PDF:", pdf_file)


if __name__ == "__main__":
    main()