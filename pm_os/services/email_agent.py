from pm_os.llm.client import LLMClient

llm = LLMClient()

def triage_email(email_subject: str, email_body: str) -> dict:
    prompt = f"SUBJECT:\n{email_subject}\n\nBODY:\n{email_body}\n"
    return llm.complete_json(
        system="You are an IR + origination analyst. Classify relevance and suggest CRM updates.",
        user=prompt,
        schema_name="RelevanceResult",
    )

