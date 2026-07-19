def chunk_pages(
    pages: list[dict],
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[dict]:
    """
    Split extracted PDF pages into overlapping word-based chunks.

    Args:
        pages: Extracted PDF pages containing page numbers and text.
        chunk_size: Maximum number of words per chunk.
        overlap: Number of words repeated between consecutive chunks.

    Returns:
        A list of dictionaries containing page, chunk number, and text.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    chunks = []
    step_size = chunk_size - overlap

    for page in pages:
        words = page["text"].split()
        chunk_number = 1

        for start in range(0, len(words), step_size):
            chunk_words = words[start : start + chunk_size]

            if not chunk_words:
                continue

            chunks.append(
                {
                    "page": page["page"],
                    "chunk": chunk_number,
                    "text": " ".join(chunk_words),
                }
            )

            chunk_number += 1

            if start + chunk_size >= len(words):
                break

    return chunks