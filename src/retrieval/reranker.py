# import chromadb

# client = chromadb.PersistentClient("./data/chromadb")
# collection = client.get_collection("knowledge_base")

# print(collection.count())
from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query,
        documents,
        top_k=8
    ):

        if not documents:
            return []

        # pairs = [
        #     (
        #         query,
        #         doc["document"]
        #     )
        #     for doc in documents
        # ]
        pairs = []

        for doc in documents:

            metadata = doc.get("metadata", {})

            enriched_document = f"""
            Source type: {metadata.get("doc_type", "")}
            Lesson: {metadata.get("lesson_title", "")}
            Day: {metadata.get("day_title", "")}
            Date: {metadata.get("date", "")}

            Content:
            {doc["document"]}
            """

            pairs.append(
                (query, enriched_document)
            )

        scores = self.model.predict(
            pairs,
            batch_size=8,
            show_progress_bar=False
        )

        for doc, score in zip(
            documents,
            scores
        ):

            doc["rerank_score"] = float(score)

        documents.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return documents[:top_k]