from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", "bot", ".env"), override=True)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

LEVEL_CHANNELS = {
    1: os.getenv("CHANID_LIV1"),
    2: os.getenv("CHANID_LIV2"),
    3: os.getenv("CHANID_LIV3"),
    4: os.getenv("CHANID_LIV4"),
}
