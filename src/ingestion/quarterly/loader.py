import json

from pathlib import Path


def load_lesson(path):

    with Path(path).open(

        "r",

        encoding="utf8"

    ) as f:

        return json.load(f)