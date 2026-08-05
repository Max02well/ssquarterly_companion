import os

from openai import OpenAI, APIConnectionError
from dotenv import load_dotenv

load_dotenv()


class LLMClient:

    def __init__(self):

        # self.client = OpenAI(
        #     base_url=os.getenv(
        #         "OLLAMA_BASE_URL",
        #         "http://localhost:11434/v1"
        #     ),
        #     api_key=os.getenv(
        #         "OLLAMA_API_KEY",
        #         "ollama"
        #     )
        # )
        base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434"
        )

        self.client = OpenAI(
            base_url=f"{base_url}/v1",
            api_key="ollama"
        )

        self.model = os.getenv(
            "OLLAMA_MODEL",
            "qwen2.5:0.5b"
        )

    def generate(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int | None = None
    ):

        try:

            kwargs = {
                "model": self.model,
                "temperature": temperature,
                "messages": [
                    # {
                    #     "role": "system",
                    #     "content": (
                    #         "You are Quarterly Companion, "
                    #         "a careful Seventh-day Adventist "
                    #         "Sabbath School study assistant. "
                    #         "Answer only from the supplied source material."
                    #     )
                    # },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            if max_tokens:
                kwargs["max_tokens"] = max_tokens

            response = self.client.chat.completions.create(
                **kwargs
            )

            return response.choices[0].message.content

        except APIConnectionError:

            return (
                "Unable to connect to the local LLM server. "
                "Make sure Ollama is running."
            )

        except Exception as e:

            return f"LLM Error: {e}"