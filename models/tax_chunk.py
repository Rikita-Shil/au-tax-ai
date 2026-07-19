from dataclasses import dataclass, field


@dataclass
class TaxChunk:
    """
    Represents one searchable chunk from an ATO document.
    """

    document_name: str
    document_year: int
    page_number: int
    chunk_number: int
    content: str
    embedding: list[float] = field(default_factory=list)


if __name__ == "__main__":

    chunk = TaxChunk(
        document_name="Guide to Capital Gains Tax",
        document_year=2025,
        page_number=1,
        chunk_number=1,
        content="Capital gains tax applies...",
    )

    print(chunk)