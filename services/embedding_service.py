import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class EmbeddingService:
    """
    Generate vector embeddings using the Gemini Embedding API.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv(
            "EMBEDDING_MODEL",
            "gemini-embedding-001",
        )
        self.dimension = int(
            os.getenv("EMBEDDING_DIMENSION", "768")
        )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing from the .env file."
            )

        self.client = genai.Client(api_key=api_key)

    def embed_document(self, text: str) -> list[float]:
        """
        Create an embedding for an ATO document chunk.
        """

        if not text.strip():
            raise ValueError("Cannot embed empty document text.")

        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=self.dimension,
            ),
        )

        return response.embeddings[0].values

    def embed_query(self, query: str) -> list[float]:
        """
        Create an embedding for a user's search query.
        """

        if not query.strip():
            raise ValueError("Cannot embed an empty query.")

        response = self.client.models.embed_content(
            model=self.model,
            contents=query,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=self.dimension,
            ),
        )

        return response.embeddings[0].values


if __name__ == "__main__":
    service = EmbeddingService()

    test_text = (
        "Australian residents may need to pay capital gains tax "
        "when they dispose of shares."
    )

    embedding = service.embed_document(test_text)

    print("Embedding created successfully.")
    print(f"Embedding dimensions: {len(embedding)}")
    print(f"First five values: {embedding[:5]}")

    