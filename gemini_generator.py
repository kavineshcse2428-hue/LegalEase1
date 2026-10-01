from google import genai
from google.genai import types
import config

SYSTEM_PROMPT = (
    "You are a legal drafting assistant. Produce complete, professionally formatted "
    "legal documents in plain text. Use numbered section headings such as '1. Services:', "
    "formal legal language, and bracketed placeholders like [Address] for unknown details. "
    "Do not use markdown symbols such as #, ** or backticks. "
    "Do not add any commentary before or after the document."
)


class GeminiDocumentGenerator:
    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Open the .env file in the LegalEase1 folder, "
                "paste your key after GEMINI_API_KEY=, save, and restart the backend."
            )
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.models = list(dict.fromkeys([config.GEMINI_MODEL] + config.FALLBACK_MODELS))

    def generate_document(self, document_type, parties, terms, dates) -> str:
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions (semicolon separated): {terms}\n"
            "Ensure formal legal structure: title, preamble, multiple numbered sections, "
            "legal clauses (governing law, severability, entire agreement, termination) "
            "and a signature block."
        )
        errors = []
        for model in self.models:
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT, temperature=0.3
                    ),
                )
                if response.text:
                    return response.text
                errors.append(f"{model}: empty response")
            except Exception as e:
                errors.append(f"{model}: {str(e)[:200]}")
        raise RuntimeError("All models failed -> " + " | ".join(errors))
