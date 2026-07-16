"""
Utilities for converting Adventech lesson HTML into clean text/markdown.
"""

import re

from bs4 import BeautifulSoup
from markdownify import markdownify


def html_to_markdown(html: str) -> str:
    """
    Convert lesson HTML to Markdown.
    """

    markdown = markdownify(
        html,
        heading_style="ATX",
        bullets="-",
        strip=["style", "script"],
    )

    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    return markdown.strip()


def html_to_text(html: str) -> str:
    """
    Convert HTML to readable plain text.
    """

    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text("\n")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()