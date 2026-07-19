from repositories.supabase_tax_chunk_repository import (
    SupabaseTaxChunkRepository,
)
from services.embedding_service import EmbeddingService


class RetrievalService:
    """
    Generate an embedding for a user's question and retrieve
    relevant ATO tax-guide chunks from Supabase.
    """

    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.repository = SupabaseTaxChunkRepository()

    def search(
        self,
        query: str,
        match_count: int = 5,
        match_threshold: float = 0.4,
    ) -> list[dict]:
        """
        Search for chunks relevant to a tax question.
        """

        cleaned_query = query.strip()

        if not cleaned_query:
            raise ValueError("The query cannot be empty.")

        query_embedding = self.embedding_service.embed_query(
            cleaned_query
        )

        return self.repository.search_similar(
            query_embedding=query_embedding,
            match_count=match_count,
            match_threshold=match_threshold,
        )


if __name__ == "__main__":
    retrieval_service = RetrievalService()

    question = (
        "Can an Australian individual claim the CGT discount "
        "when selling shares?"
    )

    results = retrieval_service.search(
        query=question,
        match_count=5,
        match_threshold=0.4,
    )

    print(f"\nQuestion: {question}")
    print(f"Results found: {len(results)}\n")

    for index, result in enumerate(results, start=1):
        print("=" * 70)
        print(f"Result {index}")
        print(f"Document: {result.get('document_name')}")
        print(f"Page: {result.get('page_number')}")
        print(f"Chunk: {result.get('chunk_number')}")
        print(f"Similarity: {result.get('similarity')}")
        print()
        print(result.get("content"))
        print()