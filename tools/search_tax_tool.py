from services.retrieval_service import RetrievalService


retrieval_service = RetrievalService()


def search_tax_guide(
    question: str,
    match_count: int = 5,
) -> dict:
    """
    Search the ATO tax guide for information relevant to a tax question.

    Args:
        question: The user's Australian tax question.
        match_count: Maximum number of matching passages to return.

    Returns:
        A dictionary containing matching ATO passages.
    """

    cleaned_question = question.strip()

    if not cleaned_question:
        return {
            "status": "error",
            "message": "The question cannot be empty.",
            "results": [],
        }

    try:
        results = retrieval_service.search(
            query=cleaned_question,
            match_count=match_count,
            match_threshold=0.4,
        )

        formatted_results = []

        for result in results:
            formatted_results.append(
                {
                    "document_name": result.get("document_name"),
                    "page_number": result.get("page_number"),
                    "chunk_number": result.get("chunk_number"),
                    "content": result.get("content"),
                    "similarity": result.get("similarity"),
                }
            )

        return {
            "status": "success",
            "question": cleaned_question,
            "results": formatted_results,
        }

    except Exception as error:
        return {
            "status": "error",
            "message": str(error),
            "results": [],
        }


if __name__ == "__main__":
    response = search_tax_guide(
        "Can an Australian individual claim the CGT discount?"
    )

    print(response)