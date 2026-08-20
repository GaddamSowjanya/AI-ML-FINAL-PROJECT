import csv
import os
from datetime import datetime

from fyers_apiv3.FyersWebsocket import data_ws

from config import (
    FYERS_APP_ID,
    FYERS_ACCESS_TOKEN,
    SYMBOL,
    LIVE_DATA_FILE
)


history = []


def save_tick(row):

    file_exists = os.path.exists(
        LIVE_DATA_FILE
    )

    with open(
        LIVE_DATA_FILE,
        "a",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "symbol",
                "ltp",
                "volume",
                "bid",
                "ask"
            ]
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)


def process_tick(message):

    if not isinstance(message, dict):
        return

    if "ltp" not in message:
        return

    ltp = message.get("ltp")

    if ltp is None:
        return

    timestamp = datetime.now().isoformat()

    row = {
        "timestamp": timestamp,
        "symbol": message.get(
            "symbol",
            SYMBOL
        ),
        "ltp": float(ltp),
        "volume": message.get(
            "vol_traded_today",
            0
        ),
        "bid": message.get(
            "bid_price",
            0
        ),
        "ask": message.get(
            "ask_price",
            0
        )
    }

    history.append(row)

    save_tick(row)

    print(
        f"[LIVE] "
        f"{row['timestamp']} | "
        f"{row['symbol']} | "
        f"LTP={row['ltp']}"
    )


def on_message(message):

    process_tick(message)


def on_error(message):

    print(
        "[WEBSOCKET ERROR]",
        message
    )


def on_close(message):

    print(
        "[WEBSOCKET CLOSED]",
        message
    )


def on_open():

    print(
        "[WEBSOCKET CONNECTED]"
    )

    fyers.subscribe(
        symbols=[SYMBOL],
        data_type="SymbolUpdate"
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
        "Starting live Fyers WebSocket..."
    )

    fyers.connect()
