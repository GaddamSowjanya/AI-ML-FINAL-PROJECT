import pandas as pd

from model import train_model


FILE = "3_data_and_model/day1/live_data.csv"


def main():

    df = pd.read_csv(FILE)

    if len(df) < 100:

        print(
            "Not enough live data to train the model."
        )

        return

    model, accuracy = train_model(df)

    print("\nModel training completed.")

    print(
        f"Test accuracy: {accuracy:.4f}"
    )


if __name__ == "__main__":
    main()
