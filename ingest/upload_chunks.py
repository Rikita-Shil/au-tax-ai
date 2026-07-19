from services.ingestion_service import IngestionService


service = IngestionService()

service.ingest_pdf(
    pdf_path="documents/ato_cgt_guide.pdf",
    document_name="Guide to Capital Gains Tax",
    document_year=2025,
)