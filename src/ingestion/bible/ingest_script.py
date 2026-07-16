from pathlib import Path

from src.ingestion.bible.loader import load_bibles
from src.ingestion.bible.parser import parse_bible
from src.ingestion.bible.chunker import chunk_documents
from src.ingestion.bible.embedder import BibleEmbedder


DATA_DIR = Path("data/raw/bible")


def ingest_all():

    embedder = BibleEmbedder()

    for file in DATA_DIR.glob("*.json"):

        print(f"Ingesting {file.name}")

        data = load_bibles(file)

        docs = parse_bible(data)

        chunks = chunk_documents(
            docs,
            verses_per_chunk=5
        )

        embedder.add_documents(chunks)


if __name__ == "__main__":

    ingest_all()