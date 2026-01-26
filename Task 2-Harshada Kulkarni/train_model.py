import sys
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("blood_donation_dataset.csv")

le = LabelEncoder()
data['blood_group'] = le.fit_transform(data['blood_group'])
data['gender'] = le.fit_transform(data['gender'])

X = data.drop('target', axis=1)
y = data['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "blood_donation_model.pkl")

print("✅ Model trained and saved successfully")
