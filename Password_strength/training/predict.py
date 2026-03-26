import pickle
import os

# Get absolute path of current file (predict.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one level up (to Password_strength folder)
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

# Correct file paths
model_path = os.path.join(ROOT_DIR, "model.pkl")
vectorizer_path = os.path.join(ROOT_DIR, "vectorizer.pkl")

# Load files safely
with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)


def predict_password(password):
    vec = vectorizer.transform([password])
    pred = model.predict(vec)[0]

    if pred == 0:
        return "Weak ❌"
    elif pred == 1:
        return "Medium ⚠️"
    else:
        return "Strong ✅"
