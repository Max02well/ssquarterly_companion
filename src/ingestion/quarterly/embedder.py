import chromadb
import re
from sentence_transformers import SentenceTransformer


class QuarterlyEmbedder:

    def __init__(self):

        self.model = SentenceTransformer(
            # "all-MiniLM-L6-v2"
            "BAAI/bge-small-en-v1.5"
        )

        client = chromadb.PersistentClient(

            path="./data/chromadb"

        )

        self.collection = client.get_or_create_collection(

            "knowledge_base"

        )

    def add_documents(self, docs):

        ids=[]

        texts=[]

        metas=[]

        embeddings=[]

        for doc in docs:
            if not doc.get("document"):
                continue

            if not doc.get("id"):
                continue

            text = re.sub(
                r"\s+",
                " ",
                doc["document"]
            ).strip()


            ids.append(doc["id"])

            # texts.append(doc["document"])
            texts.append(
                f"passage: {text}"
            )

            metas.append(doc["metadata"])
        if not texts:
            return

        embeddings=self.model.encode(
            batch_size=64,
            inputs=texts,
            normalize_embeddings=True,
            show_progress_bar=True

        ).tolist()
        
        try:
            self.collection.upsert(

                ids=ids,

                documents=texts,

                embeddings=embeddings,

                metadatas=metas
        )
            
        except Exception as e:
            print(f"Failed to add batch: {e}")
            print(f"Error upserting documents: {e}")
            # print(f"IDs: {ids}")
            # print(f"Texts: {texts}")
            # print(f"Metas: {metas}")
            # print(f"Embeddings: {embeddings}")