import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

DATA_FILE = "balanced_data.csv"
MODEL_FILE = "attack_classifier_model.pkl"

def main():
    print("\n==================== LOADING DATA ====================")
    data = pd.read_csv(DATA_FILE)

    if 'label' not in data.columns:
        raise ValueError("balanced_data.csv must contain 'label' column")

    X = data.drop('label', axis=1)
    y = data['label']

    # Encode labels if needed
    le = LabelEncoder()
    y = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    print(f"✔ Dataset shape: {data.shape}")
    print("\n==================== TRAINING MODEL ====================")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Model trained! Accuracy: {acc:.2f}")

    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    joblib.dump(clf, MODEL_FILE)
    print(f"\n📀 Model saved as '{MODEL_FILE}'")

if __name__ == "__main__":
    main()
