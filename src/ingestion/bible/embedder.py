import chromadb

from sentence_transformers import SentenceTransformer


class BibleEmbedder:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        client = chromadb.PersistentClient(
            path="./data/chromadb"
        )

        self.collection = client.get_or_create_collection(
            name="knowledge_base"
        )

    def add_documents(self, documents):

        ids = []

        texts = []

        metadatas = []

        embeddings = []

        for doc in documents:

            ids.append(doc["id"])

            texts.append(doc["document"])

            metadatas.append(doc["metadata"])

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        ).tolist()

        self.collection.upsert(

            ids=ids,

            documents=texts,

            metadatas=metadatas,

            embeddings=embeddings

        )

        print(f"Inserted {len(ids)} documents.")