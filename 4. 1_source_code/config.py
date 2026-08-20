import os
from dotenv import load_dotenv

load_dotenv()

FYERS_APP_ID = os.getenv("FYERS_APP_ID")
FYERS_ACCESS_TOKEN = os.getenv("FYERS_ACCESS_TOKEN")

SYMBOL = os.getenv("SYMBOL", "NSE:SBIN-EQ")

DATA_DIR = "3_data_and_model"
DAY1_DIR = os.path.join(DATA_DIR, "day1")
DAY2_DIR = os.path.join(DATA_DIR, "day2")
MODEL_DIR = os.path.join(DATA_DIR, "model")

LIVE_DATA_FILE = os.path.join(DAY1_DIR, "live_data.csv")
PREDICTION_FILE = os.path.join(DAY1_DIR, "live_predictions.csv")

MODEL_FILE = os.path.join(MODEL_DIR, "trained_model.pkl")

os.makedirs(DAY1_DIR, exist_ok=True)
os.makedirs(DAY2_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
