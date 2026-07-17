from collections import defaultdict

from src.retrieval.vector_search import VectorSearcher

from src.retrieval.bm25 import BM25Searcher


class HybridSearcher:

    def __init__(self):

        self.vector = VectorSearcher()

        self.bm25 = BM25Searcher()

    def search(self, query, k=10):

        vector_results = self.vector.search(

            query,
            k=20
        )

        bm25_results = self.bm25.search(

            query,
            k=20
        )

        merged = defaultdict(dict)

        for doc in vector_results:

            merged[doc["id"]] = doc

            merged[doc["id"]]["vector_score"] = doc["score"]

        for doc in bm25_results:

            if doc["id"] not in merged:

                merged[doc["id"]] = doc

            merged[doc["id"]]["bm25_score"] = doc["score"]

        docs = []

        for doc in merged.values():

            score = (

                doc.get("vector_score",0)

                +

                doc.get("bm25_score",0)

            )

            doc["hybrid_score"] = score

            docs.append(doc)

        docs.sort(

            key=lambda x:x["hybrid_score"],

            reverse=True

        )

        return docs[:k]