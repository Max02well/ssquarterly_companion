import chromadb

client = chromadb.PersistentClient("./data/chromadb")
collection = client.get_collection("knowledge_base")

print(collection.count())