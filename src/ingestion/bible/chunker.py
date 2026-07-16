from collections import defaultdict


def chunk_documents(documents, verses_per_chunk=5):

    grouped = defaultdict(list)

    for doc in documents:

        key = (
            doc["metadata"]["translation"],
            doc["metadata"]["book"],
            doc["metadata"]["chapter"]
        )

        grouped[key].append(doc)

    chunks = []

    for _, verses in grouped.items():

        verses.sort(key=lambda x: x["metadata"]["verse"])

        for i in range(0, len(verses), verses_per_chunk):

            group = verses[i:i + verses_per_chunk]

            first = group[0]["metadata"]["verse"]
            last = group[-1]["metadata"]["verse"]

            text = "\n".join(
                f'{v["metadata"]["verse"]}. {v["document"]}'
                for v in group
            )

            meta = group[0]["metadata"].copy()

            meta["verse_start"] = first
            meta["verse_end"] = last

            meta["reference"] = (
                f'{meta["book"]} {meta["chapter"]}:{first}-{last}'
            )

            chunks.append({

                "id":
                f'{meta["translation"]}_{meta["book"]}_{meta["chapter"]}_{first}_{last}',

                "document": text,

                "metadata": meta

            })

    return chunks



# def chunk_verses(verses):

#     """
#     Each verse becomes one chunk.

#     This makes scripture references
#     much easier to retrieve.

#     Returns

#     [
#         {
#             "document": "...",
#             "metadata": {...}
#         }
#     ]
#     """

#     chunks = []

#     for verse in verses:

#         meta = verse["metadata"]

#         chunks.append(

#             {

#                 "document":

#                 f"{meta['reference']} ({meta['translation']})\n\n"

#                 f"{verse['text']}",

#                 "metadata": meta

#             }

#         )

#     return chunks