import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# Base EGW Text Server URL
BASE_URL = "https://text.egwwritings.org"

# Common Book IDs to scrape
# 130 = The Desire of Ages (DA)
# 132 = The Great Controversy (GC)
# 128 = Patriarchs and Prophets (PP)
# 129 = Prophets and Kings (PK)
# 131 = Acts of the Apostles (AA)
BOOK_CONFIGS = {
    130: {"acronym": "DA", "title": "The Desire of Ages"},
    132: {"acronym": "GC", "title": "The Great Controversy"}
}

def scrape_egw_book(book_id: int, book_acronym: str, book_title: str, output_dir: str = "data/raw/egw_commentary"):
    """
    Recursively scrapes pages of an EGW book from the text.egwwritings.org site.
    Stores the output in a clean structured JSON format.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # Start at the first content page of the book
    current_page_url = f"{BASE_URL}/publication.php?pub_info_id={book_id}"
    
    scraped_paragraphs = []
    visited_urls = set()
    chapter_title = "Introduction"

    print(f"🚀 Initiating scrape for: {book_title} ({book_acronym})")

    while current_page_url and current_page_url not in visited_urls:
        print(f"Fetching page: {current_page_url}")
        visited_urls.add(current_page_url)

        try:
            response = requests.get(current_page_url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"⚠️ Failed to fetch page. Status: {response.status_code}")
                break
                
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 1. Update the current chapter title if a heading exists on this page
            heading = soup.find("h1") or soup.find("h2") or soup.find(class_="chapter")
            if heading:
                chapter_title = heading.get_text().strip()

            # 2. Extract paragraphs along with their page and paragraph metadata
            # EGW paragraphs typically reside in divs with classes like 'wrapper' or tags like <p>
            paragraphs = soup.find_all(["p", "div"], class_=re.compile(r"para|wrapper|content"))
            
            for index, p in enumerate(paragraphs):
                text = p.get_text().strip()
                if not text or len(text) < 15: # Skip small, non-narrative layout elements
                    continue
                
                # Check if the paragraph contains a standard page marker (e.g. "[120]")
                page_match = re.search(r"\[(\d+)\]", text)
                page_number = int(page_match.group(1)) if page_match else None
                
                # Clean up brackets from the visual text
                clean_text = re.sub(r"\[\d+\]", "", text).strip()
                
                scraped_paragraphs.append({
                    "book_id": book_id,
                    "book_title": book_title,
                    "acronym": book_acronym,
                    "chapter": chapter_title,
                    "page": page_number,
                    "paragraph_index": len(scraped_paragraphs) + 1,
                    "text": clean_text,
                    "citation": f"{book_acronym} {page_number if page_number else 'n/a'}.{index + 1}"
                })

            # 3. Handle Pagination - Find the "Next Page" link element
            next_link = soup.find("a", href=re.compile(r"pub_info_id="))
            # Look specifically for navigation elements containing "Next" or arrows "👉" / ">"
            all_links = soup.find_all("a", href=True)
            next_page_url = None
            
            for link in all_links:
                link_text = link.get_text().lower()
                if "next" in link_text or "▶" in link_text or ">" in link_text:
                    next_page_url = f"{BASE_URL}/{link['href']}"
                    break

            current_page_url = next_page_url
            
            # Rate limiting delay to respect target host bandwidth
            time.sleep(1.5)

        except Exception as e:
            print(f"❌ Error occurred while scraping: {e}")
            break

    # Save the crawled payload
    output_file = Path(output_dir) / f"{book_acronym.lower()}_content.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(scraped_paragraphs, f, indent=2, ensure_ascii=False)

    print(f"🎉 Scraping complete! Collected {len(scraped_paragraphs)} structured paragraph blocks.")
    print(f"Data successfully compiled to: {output_file}")


if __name__ == "__main__":
    # Start by scraping "The Desire of Ages" (Book ID 130)
    scrape_egw_book(
        book_id=130, 
        book_acronym=BOOK_CONFIGS[130]["acronym"], 
        book_title=BOOK_CONFIGS[130]["title"]
    )