import json
import os
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "ml/model.pkl"
VEC_PATH = "ml/vectorizer.pkl"


def train_model():
    with open("data/diseases.json") as f:
        data = json.load(f)

    X, y = [], []

    for disease in data:
        if disease not in ["default", "aliases"]:
            X.append(disease)
            y.append(disease)

    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vec, y)

    os.makedirs("ml", exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    with open(VEC_PATH, "wb") as f:
        pickle.dump(vectorizer, f)


def load_model():
    if not os.path.exists(MODEL_PATH):
        train_model()

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(VEC_PATH, "rb") as f:
        vectorizer = pickle.load(f)

    return model, vectorizer


def classify(disease):
    model, vectorizer = load_model()
    vec = vectorizer.transform([disease])
    return model.predict(vec)[0]