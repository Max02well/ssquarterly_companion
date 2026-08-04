from src.llm.assistant import QuarterlyCompanion


assistant = QuarterlyCompanion()


print("=" * 70)
print("Quarterly Companion AI")
print("=" * 70)


while True:

    question = input(
        "\nAsk Quarterly Companion > "
    )

    if question.lower() in {
        "exit",
        "quit"
    }:

        break

    result = assistant.ask(
        question
    )

    print("\n")
    print("=" * 70)
    print("ANSWER")
    print("=" * 70)

    print(
        result["answer"]
    )

    print("\n")
    print("=" * 70)
    print("SOURCES")
    print("=" * 70)

    for i, doc in enumerate(
        result["documents"],
        1
    ):

        metadata = doc.get(
            "metadata",
            {}
        )

        print(
            f"{i}. "
            f"{metadata.get('doc_type')} | "
            f"{metadata.get('reference', '')} | "
            f"{metadata.get('lesson_title', '')}"
        )