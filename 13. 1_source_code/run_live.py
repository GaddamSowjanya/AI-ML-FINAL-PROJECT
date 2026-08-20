import time
import pandas as pd

from live_data import (
    fyers,
    process_tick
)

from model import load_model
from signal_generator import generate_signal
from prediction_logger import save_prediction


history = []

model = None


def handle_message(message):

    global history

    if not isinstance(message, dict):
        return

    if "ltp" not in message:
        return

    row = {
        "timestamp":
            pd.Timestamp.now().isoformat(),

        "symbol":
            message.get(
                "symbol",
                "UNKNOWN"
            ),

        "ltp":
            float(message["ltp"]),

        "volume":
            message.get(
                "vol_traded_today",
                0
            ),

        "bid":
            message.get(
                "bid_price",
                0
            ),

        "ask":
            message.get(
                "ask_price",
                0
            )
    }

    history.append(row)

    print(
        f"LIVE DATA | "
        f"{row['symbol']} | "
        f"{row['ltp']}"
    )

    if len(history) >= 15:

        result = generate_signal(
            model,
            history
        )

        if result:

            print(
                f"ML SIGNAL = "
                f"{result['signal']} | "
                f"CONFIDENCE = "
                f"{result['confidence']:.2%}"
            )

            save_prediction(result)


def on_open():

    print(
        "Connected to Fyers."
    )

    fyers.subscribe(
        symbols=["NSE:SBIN-EQ"],
        data_type="SymbolUpdate"
    )

    fyers.keep_running()


def on_error(message):

    print(
        "WebSocket error:",
        message
    )


def on_close(message):

    print(
        "WebSocket closed:",
        message
    )


def main():

    global model

    print(
        "Loading trained ML model..."
    )

    model = load_model()

    print(
        "Starting live trading intelligence system..."
    )

    fyers.connect()


if __name__ == "__main__":

    main()
