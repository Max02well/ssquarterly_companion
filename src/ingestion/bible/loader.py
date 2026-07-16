# simply loads every Bible JSON file.
from pathlib import Path
import json


BIBLE_FOLDER = Path("data/raw/bible")


def load_bibles():
    """
    Loads every JSON Bible translation.

    Returns
    -------
    list
        [
            {
                "translation":"kjv",
                "data": {...}
            }
        ]
    """

    bibles = []

    for file in BIBLE_FOLDER.glob("*.json"):

        with open(file, "r", encoding="utf-8") as f:

            bibles.append(
                {
                    "translation": file.stem.upper(),
                    "data": json.load(f)
                }
            )

    return bibles