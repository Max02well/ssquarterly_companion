import chromadb

from sentence_transformers import SentenceTransformer


class VectorSearcher:

    def __init__(self):

        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

        client = chromadb.PersistentClient(
            path="./data/chromadb"
        )

        self.collection = client.get_collection(
            "knowledge_base"
        )

    def search(self, query, k=10):

        embedding = self.model.encode(
            f"query: {query}",
            normalize_embeddings=True
        ).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=k
        )

        documents = []

        for i in range(len(results["ids"][0])):

            documents.append({

                "id": results["ids"][0][i],

                "document":
                    results["documents"][0][i],

                "metadata":
                    results["metadatas"][0][i],

                "score":
                    1-results["distances"][0][i]

            })

        return documents