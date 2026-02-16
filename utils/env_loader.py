import os
from pathlib import Path
from dotenv import load_dotenv

# Always load .env from the utils/ folder — works from any CWD
_ENV_FILE = Path(__file__).parent / ".env"


def load_env():
    load_dotenv(dotenv_path=_ENV_FILE, override=True)
    return os.getenv("ENV", "dev")
