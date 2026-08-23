import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    AI_ENABLED = (
        os.getenv("AI_ENABLED", "false").lower() == "true"
    )
    AI_API_KEY = os.getenv(
        "AI_API_KEY",
        ""
    )

    OCR_ENABLED = (
        os.getenv("OCR_ENABLED", "false").lower() == "true"
    )
