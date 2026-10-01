import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)


def _clean(v: str) -> str:
    return (v or "").strip().strip('"').strip("'").strip()


GEMINI_API_KEY = _clean(os.getenv("GEMINI_API_KEY", ""))
if GEMINI_API_KEY.startswith("PASTE"):
    GEMINI_API_KEY = ""

# Model order: newest first, then safe fallbacks (there is no "3.8" model yet).
GEMINI_MODEL = _clean(os.getenv("GEMINI_MODEL", "gemini-3.6-flash"))
FALLBACK_MODELS = ["gemini-3.5-flash", "gemini-flash-latest", "gemini-2.5-flash"]

BACKEND_URL = _clean(os.getenv("BACKEND_URL", "http://localhost:8000"))

LOGO_PATH = BASE_DIR / "Image" / "Logo.png"
WEB_LOGO_PATH = BASE_DIR / "Image" / "inverseLogo.png"
FOOTER_TEXT = "LegalEase Inc. | contact@legalease.com | All Rights Reserved."
