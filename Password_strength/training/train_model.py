import pandas as pd
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ==============================
# STEP 1: HANDLE FILE PATH PROPERLY
# ==============================

# Get current file location (training folder)
base_path = os.path.dirname(__file__)

# Go to main project folder
parent_path = os.path.abspath(os.path.join(base_path, ".."))

# Dataset path
file_path = os.path.join(parent_path, "dataset_making", "password_dataset_with_users.csv")

print("📂 Loading dataset from:", file_path)

# ==============================
# STEP 2: LOAD DATASET
# ==============================
df = pd.read_csv(file_path)

print("✅ Dataset loaded successfully!")
print("Columns:", df.columns)
print(df.head())

# ==============================
# STEP 3: CLEAN & PREPARE DATA
# ==============================

# Ensure column names are correct
if 'password' not in df.columns or 'strength_label' not in df.columns:
    raise Exception("❌ Dataset must contain 'password' and 'strength_label' columns")

# Convert labels → numeric
df['strength'] = df['strength_label'].map({
    'weak': 0,
    'medium': 1,
    'strong': 2
})

# Drop missing values
df = df.dropna()

# ==============================
# STEP 4: FEATURES & LABELS
# ==============================
X = df['password']
y = df['strength']

# ==============================
# STEP 5: TEXT VECTORIZATION
# ==============================
vectorizer = TfidfVectorizer(analyzer='char')
X_vec = vectorizer.fit_transform(X)

# ==============================
# STEP 6: TRAIN MODEL
# ==============================
model = LogisticRegression(max_iter=1000)
model.fit(X_vec, y)

print("✅ Model trained successfully!")

# ==============================
# STEP 7: SAVE MODEL IN MAIN FOLDER
# ==============================
model_path = os.path.join(parent_path, "model.pkl")
vectorizer_path = os.path.join(parent_path, "vectorizer.pkl")

pickle.dump(model, open(model_path, "wb"))
pickle.dump(vectorizer, open(vectorizer_path, "wb"))

print("💾 Model saved at:", model_path)
print("💾 Vectorizer saved at:", vectorizer_path)

print("🚀 ALL DONE SUCCESSFULLY!")