import yaml
from pathlib import Path

# Anchor to project root so paths work from any CWD
PROJECT_ROOT = Path(__file__).parent.parent


class DataReader:

    @staticmethod
    def _resolve(path: str) -> Path:
        """Resolve path relative to project root — works from any working directory."""
        p = Path(path)
        return p if p.is_absolute() else PROJECT_ROOT / p

    @staticmethod
    def load_yaml(path: str):
        with open(DataReader._resolve(path), "r") as f:
            return yaml.safe_load(f)
