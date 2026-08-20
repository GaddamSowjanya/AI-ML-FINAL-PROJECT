import pandas as pd
import numpy as np


def calculate_features(df):

    df = df.copy()

    df["return_1"] = df["ltp"].pct_change()

    df["return_3"] = df["ltp"].pct_change(3)

    df["ma_5"] = df["ltp"].rolling(5).mean()

    df["ma_10"] = df["ltp"].rolling(10).mean()

    df["volatility"] = (
        df["return_1"]
        .rolling(10)
        .std()
    )

    df["ma_difference"] = (
        df["ma_5"] - df["ma_10"]
    )

    df["price_position"] = (
        df["ltp"] / df["ma_10"]
    )

    return df
