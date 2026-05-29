from utils.fallback import load_json
from ml.disease_classifier import classify

try:
    from disease_diet_adk.rag.rag_tool import query_medical_knowledge
    RAG = True
except:
    RAG = False


def extract_foods_from_text(text):

    text = text.lower()

    eat_keywords = ["eat", "recommended", "include"]
    avoid_keywords = ["avoid", "limit", "restrict"]

    eat, avoid = [], []

    lines = text.split(".")[:10]

    for line in lines:

        if any(k in line for k in eat_keywords):
            eat.append(line.strip())

        if any(k in line for k in avoid_keywords):
            avoid.append(line.strip())

    return eat[:3], avoid[:3]


def get_research(disease):

    category = classify(disease)

    data = load_json("data/diseases.json")
    base = data.get(category, data.get("default"))

    # -------------------------------
    # RAG EXTRACTION
    # -------------------------------
    if RAG:
        try:
            result = query_medical_knowledge(
                disease,
                f"foods to eat and avoid for {disease}"
            )

            if result:

                eat_extra, avoid_extra = extract_foods_from_text(result)

                return {
                    "eat": list(set(base.get("eat", []) + eat_extra)),
                    "avoid": list(set(base.get("avoid", []) + avoid_extra)),
                    "meals": base.get("meals", {}),
                    "tips": base.get("tips", []) + ["RAG-based insights added"]
                }

        except Exception as e:
            print("RAG failed:", e)

    return base