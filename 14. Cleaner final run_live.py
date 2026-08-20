import os
import csv
from datetime import datetime

from fyers_apiv3.FyersWebsocket import data_ws

from config import (
    FYERS_APP_ID,
    FYERS_ACCESS_TOKEN,
    SYMBOL,
    PREDICTION_FILE,
    LIVE_DATA_FILE
)

from model import load_model
from signal_generator import generate_signal


history = []

model = load_model()


def append_csv(filename, row):

    exists = os.path.exists(filename)

    with open(
        filename,
        "a",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=row.keys()
        )

        if not exists:
            writer.writeheader()

        writer.writerow(row)


def on_message(message):

    if not isinstance(message, dict):
        return

    if "ltp" not in message:
        return

    ltp = message["ltp"]

    if ltp is None:
        return

    row = {

        "timestamp":
            datetime.now().isoformat(),

        "symbol":
            message.get(
                "symbol",
                SYMBOL
            ),

        "ltp":
            float(ltp),

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

    append_csv(
        LIVE_DATA_FILE,
        row
    )

    print(
        f"LIVE | "
        f"{row['symbol']} | "
        f"LTP {row['ltp']}"
    )

    if len(history) < 15:

        return

    result = generate_signal(
        model,
        history
    )

    if result is None:

        return

    prediction = {

        "timestamp":
            result["timestamp"],

        "symbol":
            result["symbol"],

        "ltp":
            result["ltp"],

        "signal":
            result["signal"],

        "confidence":
            result["confidence"]
    }

    append_csv(
        PREDICTION_FILE,
        prediction
    )

    print(
        "--------------------------------"
    )

    print(
        "ML PREDICTION"
    )

    print(
        f"Signal: "
        f"{result['signal']}"
    )

    print(
        f"Confidence: "
        f"{result['confidence']:.2%}"
    )

    print(
        "--------------------------------"
    )


def on_error(message):

    print(
        "ERROR:",
        message
    )


def on_close(message):

    print(
        "CLOSED:",
        message
    )


def on_open():

    print(
        "CONNECTED TO FYERS WEBSOCKET"
    )

    fyers.subscribe(
        symbols=[SYMBOL],
        data_type="SymbolUpdate"
    )

    print(
        f"Subscribed to {SYMBOL}"
    )

    fyers.keep_running()


access_token = (
    f"{FYERS_APP_ID}:"
    f"{FYERS_ACCESS_TOKEN}"
)


fyers = data_ws.FyersDataSocket(

    access_token=access_token,

    log_path="",

    litemode=False,

    write_to_file=False,

    reconnect=True,

    on_connect=on_open,

    on_message=on_message,

    on_error=on_error,

    on_close=on_close
)


if __name__ == "__main__":

    print(
        "Starting live ML system..."
    )

    fyers.connect()
