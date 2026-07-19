import time

from google import genai
from google.genai.errors import ServerError

from services.retrieval_service import RetrievalService


class AnswerService:
    """
    Generate grounded tax answers using retrieved ATO content.
    """

    def __init__(self) -> None:
        self.client = genai.Client()
        self.model = "gemini-3.5-flash"
        self.retrieval_service = RetrievalService()

    def answer(
        self,
        question: str,
        max_retries: int = 4,
    ) -> str:
        """
        Answer a tax question using relevant ATO guide chunks.
        """

        cleaned_question = question.strip()

        if not cleaned_question:
            raise ValueError("The question cannot be empty.")

        results = self.retrieval_service.search(
            query=cleaned_question,
            match_count=5,
            match_threshold=0.4,
        )

        if not results:
            return (
                "I could not find enough relevant information "
                "in the ATO guide to answer this question."
            )

        context = self._build_context(results)
        prompt = self._build_prompt(
            question=cleaned_question,
            context=context,
        )

        return self._generate_with_retry(
            prompt=prompt,
            max_retries=max_retries,
        )

    def _generate_with_retry(
        self,
        prompt: str,
        max_retries: int,
    ) -> str:
        """
        Retry Gemini generation when the model is temporarily unavailable.
        """

        for attempt in range(1, max_retries + 1):
            try:
                print(
                    f"Generating answer "
                    f"(attempt {attempt}/{max_retries})..."
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                if not response.text:
                    return "Gemini did not return an answer."

                return response.text.strip()

            except ServerError as error:
                is_last_attempt = attempt == max_retries

                if is_last_attempt:
                    return (
                        "The retrieved ATO information was found, but "
                        "Gemini is temporarily unavailable due to high "
                        "demand. Please try again shortly.\n\n"
                        f"Technical details: {error}"
                    )

                delay_seconds = 2 ** attempt

                print(
                    "Gemini is temporarily unavailable. "
                    f"Retrying in {delay_seconds} seconds..."
                )

                time.sleep(delay_seconds)

        return "Unable to generate an answer."

    def _build_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Build the prompt supplied to Gemini.
        """

        return f"""
You are an Australian tax information assistant.

Answer the user's question using only the ATO context provided below.

Rules:
- Do not invent information.
- Do not provide personal financial or tax advice.
- Clearly explain important eligibility conditions.
- State that the response is general information only.
- Mention the relevant ATO page numbers.
- If the context is insufficient, say so clearly.
- Keep the answer clear and concise.

User question:
{question}

ATO context:
{context}
""".strip()

    def _build_context(
        self,
        results: list[dict],
    ) -> str:
        """
        Convert retrieved database rows into prompt context.
        """

        context_parts = []

        for index, result in enumerate(results, start=1):
            document_name = result.get(
                "document_name",
                "Unknown document",
            )
            page_number = result.get(
                "page_number",
                "Unknown",
            )
            content = result.get(
                "content",
                "",
            )

            context_parts.append(
                f"""
Source {index}
Document: {document_name}
Page: {page_number}
Content:
{content}
""".strip()
            )

        return "\n\n".join(context_parts)


if __name__ == "__main__":
    service = AnswerService()

    question = (
        "Can an Australian individual claim the CGT discount "
        "when selling shares?"
    )

    answer = service.answer(question)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)