from pathlib import Path

from src.ingestion.quarterly.loader import load_lesson

from src.ingestion.quarterly.parser import parse_daily_lesson

from src.ingestion.quarterly.chunker import chunk_documents

from src.ingestion.quarterly.embedder import QuarterlyEmbedder


ROOT = Path("data/raw/quarterly")


def is_daily_document(data):
    return (
        "content" in data
        and "lesson" in data
        and "lesson_title" in data
        and "date" in data
    )


def ingest():

    embedder = QuarterlyEmbedder()

    for file in ROOT.rglob("*.json"):

        lesson = load_lesson(file)
        
        if not is_daily_document(lesson):
            print(f"Skipping {file}")
            continue
        
        docs = parse_daily_lesson(lesson, file)

        chunks = chunk_documents(docs)
        
        # print(file)
        print(f"Ingesting {file.name}")
        print(f"Created {len(chunks)} chunks")


        embedder.add_documents(chunks)


if __name__ == "__main__":

    ingest()