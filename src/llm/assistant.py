from src.retrieval.retriever import Retriever
from src.llm.client import LLMClient

from src.llm.prompt import (
    build_synthesis_prompt,
    build_podcast_prompt,
    select_relevant_documents,
    deduplicate_documents
)


class QuarterlyCompanion:

    def __init__(self):

        self.retriever = Retriever()

        self.llm = LLMClient()

    def ask(
        self,
        question: str
    ):

        documents = self.retriever.search(
            question,
            k=5
        )
        
        documents = deduplicate_documents(
            documents
        )
        
        documents = select_relevant_documents(
            documents,
            max_docs=8
        )

        prompt = build_synthesis_prompt(
            question,
            documents
        )

        answer = self.llm.generate(
            prompt,
            temperature=0.1,
            max_tokens=500
        )

        return {
            "answer": answer,
            "documents": documents
        }

    def generate_podcast(
        self,
        topic: str
    ):

        documents = self.retriever.search(
            topic
        )

        prompt = build_podcast_prompt(
            topic,
            documents
        )

        script = self.llm.generate(
            prompt,
            temperature=0.3,
            max_tokens=1200
        )

        return {
            "script": script,
            "documents": documents
        }