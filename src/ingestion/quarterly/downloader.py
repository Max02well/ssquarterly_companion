import json
from pathlib import Path

import requests

BASE = "https://sabbath-school.adventech.io/api/v2/en"

OUTPUT = Path("data/raw/quarterly")

session = requests.Session()


def download_json(url):
    print(f"Get-->Downloading: {url}")

    r = session.get(url, timeout=30,headers={
        "User-Agent": "QuarterlyCompanion/1.0"
    })
    
    print("Status:", r.status_code)
    print("Content-Type:", r.headers.get("Content-Type"))

    r.raise_for_status()

    if "application/json" not in r.headers.get("Content-Type", ""):
        print(r.text[:500])
        raise Exception("Response is not JSON")

    return r.json()


def save_json(path, data):

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf8") as f:

        json.dump(data, f, indent=2, ensure_ascii=False)


def download_quarter(year: int, quarter: int):

    quarter_id = f"{year}-{quarter:02d}"

    print(f"Downloading Quarter {quarter_id}")

    # quarter_index = download_json(
    #     f"{BASE}/quarterlies/{quarter_id}/index.json"
    # )
    quarter_url = (
        f"{BASE}/quarterlies/{quarter_id}/index.json"
    )
    quarter = download_json(quarter_url)
    
    save_json(
        OUTPUT / quarter_id / "quarter.json",
        quarter
    )

    print(f"Downloaded {quarter_id}")

    for lesson in quarter.get("lessons", []):

        lesson_id = lesson["id"]

        lesson_url = (
            f"{BASE}/quarterlies/"
            f"{quarter_id}/lessons/"
            f"{lesson_id}/index.json"
        )

        lesson_json = download_json(lesson_url)

        save_json(

            OUTPUT
            / quarter_id
            / lesson_id
            / "lesson.json",

            lesson_json
        )

        print(
            f" Lesson {lesson_id} saved"
        )
   
        for day in lesson_json.get("days", []):

            # Skip entries that don't have a readable lesson
            read_url = day.get("full_read_path")

            if not read_url:
                continue

            # The API now serves the JSON from /read/index.json
            read_url = read_url.rstrip("/") + "/index.json"
            try:
                day_json = download_json(read_url)

                # Add metadata that the parser expects
                #
                day_json["year"] = year
                day_json["quarter"] = quarter
                day_json["lesson"] = lesson_id
                day_json["lesson_title"] = lesson_json["lesson"]["title"]

                save_json(
                OUTPUT
                / quarter_id
                / lesson_id
                / f"{day['id']}.json",
                day_json
                )
                print(f"      ✓ Day {day['id']} saved")

            except Exception as e:
               print(f"      ✗ Failed {day['id']}: {e}")
            # print(f"      Day {day['id']} saved")

if __name__ == "__main__":

    download_quarter(year=2026, quarter=3)