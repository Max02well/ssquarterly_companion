from src.retrieval.hybrid_search import HybridSearcher


class Retriever:

    def __init__(self):

        self.searcher = HybridSearcher()

    def search(self, question):

        return self.searcher.search(

            question,

            k=8

        )