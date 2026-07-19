from database.supabase_client import get_supabase_client
from models.tax_chunk import TaxChunk


class SupabaseTaxChunkRepository:
    """
    Repository responsible for storing and retrieving TaxChunk records
    from the Supabase tax_guide_chunks table.
    """

    TABLE_NAME = "tax_guide_chunks"

    def __init__(self) -> None:
        self.client = get_supabase_client()

    def save(self, chunk: TaxChunk) -> None:
        """
        Save or update one TaxChunk.
        """

        self._validate_chunk(chunk)

        row = self._chunk_to_row(chunk)

        self.client.table(self.TABLE_NAME).upsert(
            row,
            on_conflict="document_name,page_number,chunk_number",
        ).execute()

    def save_many(self, chunks: list[TaxChunk]) -> None:
        """
        Save or update multiple TaxChunk objects.
        """

        if not chunks:
            return

        rows = []

        for chunk in chunks:
            self._validate_chunk(chunk)
            rows.append(self._chunk_to_row(chunk))

        self.client.table(self.TABLE_NAME).upsert(
            rows,
            on_conflict="document_name,page_number,chunk_number",
        ).execute()

    def get_existing_chunk_keys(
        self,
        document_name: str,
    ) -> set[tuple[int, int]]:
        """
        Return existing page/chunk pairs.
        """

        response = (
            self.client.table(self.TABLE_NAME)
            .select("page_number,chunk_number")
            .eq("document_name", document_name)
            .execute()
        )

        return {
            (
                row["page_number"],
                row["chunk_number"],
            )
            for row in response.data
        }

    def search_similar(
        self,
        query_embedding: list[float],
        match_count: int = 5,
        match_threshold: float = 0.5,
    ) -> list[dict]:
        """
        Search the vector database for similar chunks.
        """

        if not query_embedding:
            raise ValueError("query_embedding cannot be empty.")

        response = self.client.rpc(
            "match_tax_guide_chunks",
            {
                "query_embedding": query_embedding,
                "match_threshold": match_threshold,
                "match_count": match_count,
            },
        ).execute()

        return response.data or []

    def _validate_chunk(self, chunk: TaxChunk) -> None:
        """
        Validate a TaxChunk before saving.
        """

        if not chunk.document_name.strip():
            raise ValueError("document_name cannot be empty.")

        if chunk.document_year <= 0:
            raise ValueError("document_year must be greater than zero.")

        if chunk.page_number <= 0:
            raise ValueError("page_number must be greater than zero.")

        if chunk.chunk_number <= 0:
            raise ValueError("chunk_number must be greater than zero.")

        if not chunk.content.strip():
            raise ValueError("content cannot be empty.")

        if not chunk.embedding:
            raise ValueError(
                "The chunk must have an embedding before it can be saved."
            )

    def _chunk_to_row(self, chunk: TaxChunk) -> dict:
        """
        Convert a TaxChunk into a Supabase row.
        """

        return {
            "document_name": chunk.document_name,
            "document_year": chunk.document_year,
            "page_number": chunk.page_number,
            "chunk_number": chunk.chunk_number,
            "content": chunk.content,
            "embedding": chunk.embedding,
        }


if __name__ == "__main__":
    from services.embedding_service import EmbeddingService

    embedding_service = EmbeddingService()
    repository = SupabaseTaxChunkRepository()

    test_content = (
        "Australian residents may need to pay capital gains tax "
        "when they dispose of shares."
    )

    test_chunk = TaxChunk(
        document_name="Repository Connection Test",
        document_year=2025,
        page_number=1,
        chunk_number=1,
        content=test_content,
        embedding=embedding_service.embed_document(test_content),
    )

    repository.save(test_chunk)

    existing_keys = repository.get_existing_chunk_keys(
        "Repository Connection Test"
    )

    print("Test chunk saved successfully.")
    print(f"Existing chunk keys: {existing_keys}")