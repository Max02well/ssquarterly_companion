from collections import defaultdict

from src.retrieval.vector_search import VectorSearcher

from src.retrieval.bm25 import BM25Searcher


class HybridSearcher:

    def __init__(self):

        self.vector = VectorSearcher()
        self.bm25 = BM25Searcher()

    def search(self, query, k=20,candidate_k=20):

        vector_results = self.vector.search(
            query,
            k=candidate_k
        )

        bm25_results = self.bm25.search(
            query,
            k=candidate_k
        )
        
        return self._rrf(
            vector_results,
            bm25_results,
            k=k
        )
        
    def _rrf(
            self,
            vector_results,
            bm25_results,
            k=30,
            rrf_k=40
    ):

        # merged = defaultdict(dict)
        merged = {}
        
        # Vector rankings
        for rank, doc in enumerate(
            vector_results,
            start=1
        ):
            doc_id = doc["id"]
            if doc_id not in merged:
                merged[doc_id] = {
                    **doc,
                    "vector_rank": rank,
                    "bm25_rank": None,
                    "rrf_score": 0.0
                }
                
            else:
                merged[doc_id]["vector_rank"] = rank
            merged[doc_id]["rrf_score"] += (
                1 / (rrf_k + rank)
            )

        # BM25 rankings
        for rank, doc in enumerate(
            bm25_results,
            start=1
        ):
            doc_id = doc["id"]
            if doc_id not in merged:
                merged[doc_id] = {
                    **doc,
                    "vector_rank": None,
                    "bm25_rank": rank,
                    "rrf_score": 0.0
                }
                # print(f"Doc ID: {doc_id}, Rank: {rank}, RRF Score: {merged[doc_id]['rrf_score']}")
            else:
                merged[doc_id]["bm25_rank"] = rank
            merged[doc_id]["rrf_score"] += (
                1 / (rrf_k + rank)
            )
        #sort by rrf_score and return top k
        results = list(
            merged.values()
        )
        results.sort(
            key=lambda x: x["rrf_score"],
            reverse=True
        )
        # Debug
        for rank, doc in enumerate(
            results[:k],
            start=1
        ):

            print(
                f"{rank}. "
                f"ID={doc['id']} | "
                f"RRF={doc['rrf_score']:.6f} | "
                f"VectorRank={doc['vector_rank']} | "
                f"BM25Rank={doc['bm25_rank']}"
            )

        return results[:k]
     
        

        # for doc in vector_results:

        #     merged[doc["id"]] = doc

        #     merged[doc["id"]]["vector_score"] = doc["score"]

        # for doc in bm25_results:

        #     if doc["id"] not in merged:

        #         merged[doc["id"]] = doc

        #     merged[doc["id"]]["bm25_score"] = doc["score"]

        # docs = []

        # for doc in merged.values():

        #     score = (

        #         doc.get("vector_score",0)

        #         +

        #         doc.get("bm25_score",0)

        #     )

        #     doc["hybrid_score"] = score

        #     docs.append(doc)

        # docs.sort(

        #     key=lambda x:x["hybrid_score"],

        #     reverse=True

        # )

        # return docs[:k]