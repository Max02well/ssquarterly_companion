from pathlib import Path
import joblib
from rank_bm25 import BM25Okapi

INDEX_FILE = Path("data/indexes/bm25.pkl")

bm25 = None
documents = []
metadata = []
ids = []


class BM25Searcher:

    def __init__(self):
        load_bm25()

    def search(self, query, k=10):
        return bm25_search(query, k)


def build_bm25(chunks):
    """
    Build the BM25 index from chunk dictionaries.
    """
    global ids
    global bm25
    global documents
    global metadata

    ids = [
        chunk["id"]
        for chunk in chunks
    ]
    documents = [
        chunk["document"]
        for chunk in chunks
    ]

    metadata = [
        chunk["metadata"]
        for chunk in chunks
    ]

    tokenized = [
        doc.lower().split()
        for doc in documents
    ]

    bm25 = BM25Okapi(tokenized)

    INDEX_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        {
            "ids": ids,
            "bm25": bm25,
            "documents": documents,
            "metadata": metadata,            
        },
        INDEX_FILE,
    )

    print(f"BM25 indexed {len(documents)} chunks.")
    print(f"Saved BM25 index to {INDEX_FILE}")


def load_bm25():
    global ids
    global bm25
    global documents
    global metadata

    if not INDEX_FILE.exists():
        raise FileNotFoundError(
            "BM25 index not found. Run ingestion first."
        )

    data = joblib.load(INDEX_FILE)
 
    bm25 = data["bm25"]
    ids = data["ids"]
    documents = data["documents"]
    metadata = data["metadata"]

    print(f"Loaded BM25 index ({len(documents)} chunks)")


def bm25_search(query, k=10):

    if bm25 is None:
        raise RuntimeError(
            "BM25 index has not been built."
        )

    scores = bm25.get_scores(
        query.lower().split()
    )

    ranked = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True,
    )[:k]

    results = []

    for index, score in ranked:

        results.append(
            {
                "id": ids[index],
                "document": documents[index],
                "metadata": metadata[index],
                "score": float(score),
                "source": "bm25",
            }
        )

    return results