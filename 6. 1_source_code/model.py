import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from features import calculate_features
from config import MODEL_FILE


FEATURE_COLUMNS = [
    "return_1",
    "return_3",
    "ma_5",
    "ma_10",
    "volatility",
    "ma_difference",
    "price_position"
]


def create_training_dataset(df):

    df = calculate_features(df)

    # Future price movement
    df["future_price"] = df["ltp"].shift(-5)

    # 1 = price goes up
    # 0 = price does not go up
    df["target"] = (
        df["future_price"] > df["ltp"]
    ).astype(int)

    df = df.dropna()

    return df


def train_model(df):

    df = create_training_dataset(df)

    X = df[FEATURE_COLUMNS]
    y = df["target"]

    split = int(len(df) * 0.8)

    X_train = X.iloc[:split]
    X_test = X.iloc[split:]

    y_train = y.iloc[:split]
    y_test = y.iloc[split:]

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(
        f"Training/Test Accuracy: {accuracy:.4f}"
    )

    joblib.dump(model, MODEL_FILE)

    return model, accuracy


def load_model():

    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(
            "trained_model.pkl not found. "
            "Run train_model.py first."
        )

    return joblib.load(MODEL_FILE)


def predict(model, feature_row):

    X = feature_row[FEATURE_COLUMNS]

    prediction = model.predict(X)[0]

    probabilities = model.predict_proba(X)[0]

    confidence = max(probabilities)

    if prediction == 1:
        signal = "BUY"
    else:
        signal = "SELL"

    return signal, float(confidence)
