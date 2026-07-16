def parse_bible(data):

    translation = data["translation"]

    documents = []

    for book in data["books"]:

        book_name = book["name"]

        for chapter in book["chapters"]:

            chapter_number = chapter["chapter"]

            for verse in chapter["verses"]:

                verse_number = verse["verse"]

                text = verse["text"].strip()

                documents.append({

                    "id":
                    f"{translation}_{book_name}_{chapter_number}_{verse_number}",

                    "document": text,

                    "metadata": {

                        "doc_type": "bible",

                        "translation": translation,

                        "book": book_name,

                        "chapter": chapter_number,

                        "verse": verse_number,

                        "reference":
                        f"{book_name} {chapter_number}:{verse_number}"

                    }

                })

    return documents


# import json
# from pathlib import Path

# def ingest_bible_json(json_path: str) -> list[dict]:
#     """
#     Parses a nested Bible JSON and returns a flat list of documents 
#     with chunked texts and precise metadata for your vector store.
#     """
#     with open(json_path, 'r', encoding='utf-8') as f:
#         bible_data = json.load(f)
    
#     documents = []
    
#     # Expected structure: {"Genesis": {"1": {"1": "In the beginning..."}}}
#     for book_name, chapters in bible_data.items():
#         for chapter_num, verses in chapters.items():
#             for verse_num, verse_text in verses.items():
                
#                 # We compile metadata to enable fast filtering in your RAG app
#                 metadata = {
#                     "doc_type": "bible",
#                     "translation": "KJV",
#                     "book": book_name,
#                     "chapter": int(chapter_num),
#                     "verse": int(verse_num),
#                     "reference": f"{book_name} {chapter_num}:{verse_num}"
#                 }
                
#                 # Constructing the document chunk
#                 documents.append({
#                     "id": f"KJV_{book_name.replace(' ', '_')}_{chapter_num}_{verse_num}",
#                     "text": f"[{book_name} {chapter_num}:{verse_num}] {verse_text}",
#                     "metadata": metadata
#                 })
                
#     return documents

# # Example usage:
# if __name__ == "__main__":
#     bible_file = "data/raw/bible/kjv.json"
    
#     if Path(bible_file).exists():
#         flat_bible_verses = ingest_bible_json(bible_file)
#         print(f"Parsed {len(flat_bible_verses)} verses successfully!")
#         print("Sample Data:", flat_bible_verses[0])
#     else:
#         print(f"Place your downloaded KJV JSON file at: {bible_file}")