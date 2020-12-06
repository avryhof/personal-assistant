import os
from pathlib import Path

from personal_assistant.constants import RECOGNIZER_WIT

BASE_DIR = Path(__file__).resolve().parent

# RECOGNITION_ENGINE = RECOGNIZER_SNOWBOY
# RECOGNITION_ENGINE = RECOGNIZER_SPHINX
RECOGNITION_ENGINE = RECOGNIZER_WIT

WIT_AI_KEY = os.environ.get("WIT_ACCESS_TOKEN")

TUYA_CLIENT_ID = "acmn8staa0kr86vyadd4"
TUYA_CLIENT_SECRET = "f5d87339955b451f9ba0e27de2089717"
TUYA_CHANNEL_ID = "amostest"

SUBSONIC_URL = "http://subsonic.vryhof.net:4040"
SUBSONIC_USER = "googlehome"
SUBSONIC_PASSWORD = "googlehome"

SKILLS_REGISTRY = []
