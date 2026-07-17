from src.retrieval.retriever import Retriever

#This is the CLI for the quarterly companion search.
# It allows users to input a question and receive relevant documents from the quarterly companion database.
retriever = Retriever()

print("="*60)
print("Quarterly Companion Search")
print("="*60)

while True:

    query = input("\nQuestion: ")

    if query.lower() in [

        "quit",

        "exit"

    ]:

        break

    results = retriever.search(query)

    print()

    for i,doc in enumerate(results,1):

        print("="*70)

        print(i)

        print(doc["metadata"])

        print()

        print(doc["document"][:500])

        print()