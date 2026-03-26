import pickle
import os

# Get current file path
base_path = os.path.dirname(__file__)

# Go to parent folder (Password_strength)
parent_path = os.path.abspath(os.path.join(base_path, ".."))

# Load model correctly
model = pickle.load(open(os.path.join(parent_path, "model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(parent_path, "vectorizer.pkl"), "rb"))

def predict_password(password):
    vec = vectorizer.transform([password])
    pred = model.predict(vec)[0]

    if pred == 0:
        return "Weak ❌"
    elif pred == 1:
        return "Medium ⚠️"
    else:
        return "Strong ✅"