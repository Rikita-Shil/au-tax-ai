from ingest.extract_text import extract_pdf_text
from ingest.chunk_text import chunk_pages

from models.tax_chunk import TaxChunk
from repositories.supabase_tax_chunk_repository import (
    SupabaseTaxChunkRepository,
)
from services.embedding_service import EmbeddingService


class IngestionService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.repository = SupabaseTaxChunkRepository()

    def ingest_pdf(
        self,
        pdf_path: str,
        document_name: str,
        document_year: int,
    ):

        print("Reading PDF...")

        pages = extract_pdf_text(pdf_path)

        print(f"Extracted {len(pages)} pages.")

        print("Chunking...")

        chunks = chunk_pages(
            pages,
            chunk_size=500,
            overlap=50,
        )

        print(f"Created {len(chunks)} chunks.")

        print("Generating embeddings...")

        tax_chunks = []

        total_chunks = len(chunks)

        for index, chunk in enumerate(chunks, start=1):

            print(f"Embedding {index}/{total_chunks}")

            embedding = self.embedding_service.embed_document(
                chunk["text"]
            )

            tax_chunks.append(
                TaxChunk(
                    document_name=document_name,
                    document_year=document_year,
                    page_number=chunk["page"],
                    chunk_number=chunk["chunk"],
                    content=chunk["text"],
                    embedding=embedding,
                )
            )

        print("Uploading to Supabase...")

        self.repository.save_many(tax_chunks)

        print("Finished!")