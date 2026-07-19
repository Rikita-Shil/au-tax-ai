from abc import ABC, abstractmethod

from models.tax_chunk import TaxChunk


class TaxChunkRepository(ABC):
    """
    Abstract repository for storing and retrieving tax document chunks.
    """

    @abstractmethod
    def save(self, chunk: TaxChunk):
        """Save a single chunk."""
        pass

    @abstractmethod
    def save_many(self, chunks: list[TaxChunk]):
        """Save multiple chunks."""
        pass

    @abstractmethod
    def search(
        self,
        embedding: list[float],
        limit: int = 5,
    ) -> list[TaxChunk]:
        """Return the most similar chunks."""
        pass