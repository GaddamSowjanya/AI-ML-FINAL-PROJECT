import pandas as pd


def evaluate_predictions(
    predictions_file,
    output_file
):

    df = pd.read_csv(
        predictions_file
    )

    if df.empty:

        print(
            "No predictions found."
        )

        return

    df["future_ltp"] = (
        df["ltp"].shift(-5)
    )

    df = df.dropna()

    df["actual_direction"] = (
        df["future_ltp"] >
        df["ltp"]
    ).map({
        True: "BUY",
        False: "SELL"
    })

    df["correct"] = (
        df["signal"] ==
        df["actual_direction"]
    )

    success_rate = (
        df["correct"].mean()
        * 100
    )

    result = pd.DataFrame({

        "total_predictions": [
            len(df)
        ],

        "correct_predictions": [
            int(df["correct"].sum())
        ],

        "incorrect_predictions": [
            int((~df["correct"]).sum())
        ],

        "success_rate_percent": [
            success_rate
        ],

        "average_confidence": [
            df["confidence"].mean()
            * 100
        ]
    })

    result.to_csv(
        output_file,
        index=False
    )

    print("\nEvaluation Result")

    print(result.to_string(
        index=False
    ))

    return result
