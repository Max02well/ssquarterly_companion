import hashlib

from src.ingestion.quarterly.clean_html import html_to_text


def extract_bible_documents(data):
    """
    Convert embedded Bible verses into standalone RAG documents.
    """
    seen = set()
    documents = []

    for version in data.get("bible", []):
        
        translation = version.get("name", "Unknown")

        # version_name = version.get("name", "")

        for reference, html in version.get("verses", {}).items():
            
            text = html_to_text(html).strip()
            
            # Create a stable unique hash
            uid = hashlib.md5(
                f"{data['index']}{translation}{reference}{text}".encode("utf-8")
            ).hexdigest()[:12]

            if uid in seen:
                continue

            seen.add(uid)
            
            documents.append({            
                # "id":
                #     f"{data['index']}_{reference}",
                "id": f"{data['index']}_bible_{uid}",

                # "document": text,
                "document": f"{reference}\n\n{text}",

                "metadata":{

                    "doc_type":"bible",

                    "translation":translation,

                    "reference":reference,
                                            
                    "quarter_id": data["quarter"]["quarterly"]["id"],
                    
                    "quarter_title": data["quarter"]["quarterly"]["title"],

                    "lesson": data["lesson"],
                    
                    "lesson_title": data["lesson_title"],

                    "day": data["id"],
                    
                    "day_title": data["title"],

                    "date": data["date"],
                }

            })

    return documents



# import re

# # Common Bible books
# BOOKS = [
#     "Genesis","Exodus","Leviticus","Numbers","Deuteronomy",
#     "Joshua","Judges","Ruth","1 Samuel","2 Samuel",
#     "1 Kings","2 Kings","1 Chronicles","2 Chronicles",
#     "Ezra","Nehemiah","Esther","Job","Psalms","Psalm",
#     "Proverbs","Ecclesiastes","Song of Solomon","Isaiah",
#     "Jeremiah","Lamentations","Ezekiel","Daniel","Hosea",
#     "Joel","Amos","Obadiah","Jonah","Micah","Nahum",
#     "Habakkuk","Zephaniah","Haggai","Zechariah","Malachi",

#     "Matthew","Mark","Luke","John","Acts","Romans",
#     "1 Corinthians","2 Corinthians","Galatians",
#     "Ephesians","Philippians","Colossians",
#     "1 Thessalonians","2 Thessalonians",
#     "1 Timothy","2 Timothy","Titus","Philemon",
#     "Hebrews","James","1 Peter","2 Peter",
#     "1 John","2 John","3 John","Jude","Revelation"
# ]

# pattern = re.compile(

#     rf"\b({'|'.join(map(re.escape, BOOKS))})\s+"
#     r"(\d+):(\d+(?:-\d+)?)",

#     flags=re.IGNORECASE
# )


# def extract_bible_references(text: str):

#     references = []

#     for match in pattern.finditer(text):

#         book = match.group(1)

#         chapter = match.group(2)

#         verse = match.group(3)

#         references.append(
#             f"{book} {chapter}:{verse}"
#         )

#     return sorted(set(references))