from bs4 import BeautifulSoup

from src.ingestion.quarterly.extractor import extract_bible_documents

from src.ingestion.quarterly.clean_html import (
    html_to_markdown,
    html_to_text,
)
from src.ingestion.quarterly.extractor import extract_bible_documents
from pathlib import Path




def parse_daily_lesson(data,file):

    documents = []

    html = data.get("content","")
    
    markdown = html_to_markdown(html)

    text = html_to_text(html)
    
    doc_type = Path(file).stem

    # text = BeautifulSoup(

    #         html,

    #         "html.parser"

    # ).get_text("\n")


    # references = extract_bible_documents(text)
    # references = []

    documents.append({

        "id": data["index"],
        "document": markdown,
        "text": text,
        "html": html,

        # "metadata": {

        #     "doc_type": "quarterly",

        #     "year": data["year"],

        #     "quarter": data["quarter"],

        #     "lesson": data["lesson"],

        #     "lesson_title": data["lesson_title"],

        #     "day": data["title"],

        #     "date": data["date"],

        #     "url": data.get("url", ""),

        #     "bible_references": references

        # }
        "metadata": {
                "doc_type": "lesson",
                "quarter_id": data["quarter"]["quarterly"]["id"],

                "quarter_title": data["quarter"]["quarterly"]["title"],

                "lesson": data["lesson"],

                "lesson_title": data["lesson_title"],

                "day": data["id"],

                "day_title": data["title"],

                "date": data["date"],

                "type": doc_type,
                
                # "bible_references": references
                

                }

    })
    
    # return documents
    documents.extend(
        extract_bible_documents(data)
    )

    return documents