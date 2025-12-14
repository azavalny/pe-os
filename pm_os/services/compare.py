from rapidfuzz import fuzz
from pm_os.llm.client import LLMClient
llm = LLMClient()

def similarity(a: str, b: str) -> float:
    return round(fuzz.token_set_ratio(a, b) / 100.0, 3)

def compare_docs(doc_a: str, doc_b: str) -> dict:
    prompt = f"DOC_A:\n{doc_a[:4000]}\n\nDOC_B:\n{doc_b[:4000]}\n"
    return llm.complete_json(
        system="You compare legal/IC documents. Output what changed and risk flags.",
        user=prompt,
        schema_name="DocCompareResult",
    )

