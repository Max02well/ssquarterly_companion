def _format_documents(documents):

    if not documents:
        return "No supporting sources were retrieved."

    sections = []

    for i, doc in enumerate(documents, 1):

        metadata = doc.get("metadata", {})

        source_type = metadata.get(
            "doc_type",
            "unknown"
        )

        sections.append(
            f"""
SOURCE {i}
Type: {source_type}
Metadata: {metadata}
REFERENCE: {metadata.get('reference', '')}
LESSON: {metadata.get('lesson_title', '')}
DATE: {metadata.get('date', '')}

Content:
{doc.get("document", "")}
"""
        )

    return "\n\n".join(sections)

def deduplicate_documents(documents):

    seen = set()
    unique = []

    for doc in documents:

        metadata = doc.get("metadata", {})

        key = (
            metadata.get("doc_type"),
            metadata.get("reference"),
            metadata.get("lesson_title"),
            doc.get("document", "").strip()
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(doc)

    return unique

def select_relevant_documents(documents, max_docs=8):

    lessons = []
    bible = []
    egw = []

    for doc in documents:
        doc_type = doc.get("metadata", {}).get("doc_type", "")

        if doc_type == "lesson":
            lessons.append(doc)

        elif doc_type == "bible":
            bible.append(doc)

        elif doc_type in {"egw", "ellen_white"}:
            egw.append(doc)

    selected = (
        lessons[:3]
        + bible[:3]
        + egw[:2]
    )

    return selected[:max_docs]

def build_synthesis_prompt(
    question,
    documents
):
    documents = deduplicate_documents(documents)

    documents = select_relevant_documents(
        documents,
        max_docs=6
    )
    
    context = _format_documents(documents)

    return f"""
You are Quarterly Companion, an assistant for studying
Seventh-day Adventist Sabbath School lessons.

Your task is to answer the user's question,not to reproduce
the retrieved sources.

You MUST use the retrieved sources as evidence for your answer.
SOURCE PRIORITY

==============================

QUESTION

{question}

RETRIEVED SOURCES

==============================

{context}

==============================

========================
HOW TO ANSWER
========================

First determine exactly what the user is asking.

Then use the retrieved sources to construct a direct answer.

IMPORTANT:

1. Answer the question directly in the FIRST paragraph and do not reinterpret, rewrite, broaden, or replace the question.

2. Do NOT simply copy or reproduce a Bible passage.

3. Do NOT begin your answer with "Passage:".

4. Do NOT begin by repeating the question.

5. Explain WHAT the source means in relation to the question.

6. Use the Quarterly lesson to explain the lesson's teaching.

7. Use Scripture as biblical support.

8. Use EGW material only if it was actually retrieved.

9. Do not invent information.

10. Do not invent Bible references.

11. Do not invent EGW quotations or references.

12. If the retrieved material does not adequately answer the
question, say:
"The retrieved sources do not provide enough information to
answer this fully."

13. Do not mention retrieval, chunks, rankings, embeddings,
documents, or the LLM.

14. Do not reproduce long passages from the sources.

15. Paraphrase the sources and quote only short phrases when
necessary.

========================
SOURCE PRIORITY
========================

Use sources in this order:

1. Quarterly lesson
2. Bible
3. Ellen G. White

The Quarterly lesson should normally provide the main explanation.
Scripture should provide the biblical foundation.

========================
RESPONSE FORMAT
========================

### Answer

Give a direct, natural answer in 1-3 paragraphs.

### Biblical Foundation

Explain the relevant Scripture and give the reference.

### Quarterly Connection

Explain how the lesson material develops or applies the answer.

### Key Takeaway

Give one concise practical or spiritual takeaway.

Only include an EGW section if actual EGW material was retrieved.

========================
FINAL CHECK
========================

Before answering, silently check:

- Did I answer the actual question?
- Did I explain rather than merely quote?
- Is every factual claim supported by the sources?
- Did I avoid inventing references?
- Did I avoid repeating the retrieved passage?
"""


def build_podcast_prompt(
    topic,
    documents,
    hosts=("Host 1", "Host 2")
):

    context = _format_documents(documents)

    host_a, host_b = hosts

    return f"""
You are creating a Sabbath School study podcast.

The podcast must be based ONLY on the retrieved
Quarterly lesson, Bible, and Ellen G. White material.

TOPIC

{topic}

SOURCE MATERIAL

==============================

{context}

==============================

HOSTS

{host_a}
{host_b}

RULES

- Do not invent theological claims.
- Do not fabricate quotations.
- Do not fabricate Bible references.
- Do not fabricate EGW references.
- Clearly distinguish between the Quarterly lesson,
  Scripture, and EGW material.
- Make the conversation natural and educational.
- Do not simply read the retrieved chunks word-for-word.
- Explain the ideas conversationally.
- Ask thoughtful questions between hosts.
- Keep the discussion faithful to the supplied sources.

FORMAT

{host_a}: ...

{host_b}: ...

Continue as a natural conversation.

End with a concise spiritual takeaway.
"""