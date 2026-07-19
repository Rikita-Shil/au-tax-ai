import fitz

from ingest.chunk_text import chunk_pages


def extract_pdf_text(pdf_path: str):
    """
    Read a PDF and return the text from each page.

    Returns:
        list[dict]: A list of dictionaries containing:
            - page: Page number starting from 1
            - text: Extracted text from that page
    """

    doc = fitz.open(pdf_path)
    pages = []

    for i in range(doc.page_count):
        page = doc[i]
        text = page.get_text()

        if text.strip():
            pages.append(
                {
                    "page": i + 1,
                    "text": text.strip(),
                }
            )

    doc.close()

    return pages


if __name__ == "__main__":
    pdf_pages = extract_pdf_text("documents/ato_cgt_guide.pdf")

    print(f"Extracted {len(pdf_pages)} pages.")

    chunks = chunk_pages(
        pdf_pages,
        chunk_size=500,
        overlap=50,
    )

    print(f"Created {len(chunks)} chunks.")

    if chunks:
        print("\nFirst chunk:\n")
        print(chunks[0])