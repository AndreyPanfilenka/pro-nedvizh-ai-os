from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_BASE_URL: str = os.getenv(
    "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
)
OPENROUTER_TIMEOUT: int = int(os.getenv("OPENROUTER_TIMEOUT", "120"))
APP_NAME: str = os.getenv("APP_NAME", "PRO Nedvizh AI OS")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
