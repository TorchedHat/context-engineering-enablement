"""Read the wheel catalog in data/catalog.json."""
import json
from pathlib import Path

CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "catalog.json"


def load_catalog():
    with CATALOG_PATH.open() as f:
        return json.load(f)


def wheels_for(package, oven=None):
    """All catalog entries for a package, optionally filtered by oven."""
    return [
        w for w in load_catalog()["wheels"]
        if w["package"] == package and (oven is None or w["oven"] == oven)
    ]


def burnt_wheels(threshold):
    """Wheels whose consecutive failure count is at or above threshold."""
    return [w for w in load_catalog()["wheels"] if w["consecutive_failures"] >= threshold]
