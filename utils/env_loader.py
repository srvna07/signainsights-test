import os
from pathlib import Path
from dotenv import load_dotenv

_ENV_FILE = Path(__file__).parent.parent / ".env"


def load_env():
    load_dotenv(dotenv_path=_ENV_FILE, override=True)
    return os.getenv("ENV", "dev")
