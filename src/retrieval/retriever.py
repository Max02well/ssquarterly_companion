from src.retrieval.hybrid_search import HybridSearcher
from src.retrieval.reranker import Reranker


class Retriever:

    def __init__(self):

        self.searcher = HybridSearcher()
        self.reranker = Reranker()

    def search(self, question,k=8):
        
        candidates = self.searcher.search(
            question,
            k=20,
            candidate_k=20
        )
        
        return self.reranker.rerank(
            question,
            documents=candidates,
            top_k=k
        )