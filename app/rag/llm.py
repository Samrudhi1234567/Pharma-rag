import os

from huggingface_hub import InferenceClient

from app.rag.config import LLM_MODEL, LLM_PROVIDER


class LLMService:
    """
    LLM service for generating grounded answers from retrieved context.
    """

    def __init__(self):
        self.provider = LLM_PROVIDER
        self.model = LLM_MODEL

        if self.provider == "huggingface":
            hf_token = os.getenv("HF_TOKEN")

            if not hf_token:
                raise ValueError(
                    "HF_TOKEN is required when LLM_PROVIDER is huggingface"
                )

            self.client = InferenceClient(
                api_key=hf_token
            )

    def generate(
        self,
        *,
        query: str,
        context: str,
    ) -> str:
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        if not context or not context.strip():
            return (
                "I could not find enough information in the "
                "provided pharmaceutical documents to answer this question."
            )

        if self.provider == "huggingface":
            response = self.client.chat_completion(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a pharmaceutical information assistant. "
                            "Answer the user's question using only the "
                            "information provided in the retrieved context. "
                            "Do not invent or assume facts that are not present "
                            "in the context. If the context does not contain "
                            "enough information to answer the question, "
                            "clearly say that the information is not available "
                            "in the provided documents. "
                            "Give a concise and direct answer."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Retrieved pharmaceutical context:\n\n"
                            f"{context}\n\n"
                            f"Question: {query}"
                        ),
                    },
                ],
                max_tokens=300,
                temperature=0.1,
            )

            return response.choices[0].message.content.strip()

        if self.provider == "mock":
            return (
                "Based on the provided pharmaceutical documents, "
                f"the answer to your question is related to: {query}"
            )

        raise ValueError(
            f"Unsupported LLM provider: {self.provider}"
        )