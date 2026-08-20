import pandas as pd

from features import calculate_features
from model import predict


def generate_signal(model, history):

    if len(history) < 15:
        return None

    df = pd.DataFrame(history)

    df = calculate_features(df)

    latest = df.iloc[-1:]

    signal, confidence = predict(
        model,
        latest
    )

    return {
        "timestamp": latest["timestamp"].iloc[0],
        "symbol": latest["symbol"].iloc[0],
        "ltp": latest["ltp"].iloc[0],
        "signal": signal,
        "confidence": confidence
    }
