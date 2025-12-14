from pm_os.llm.client import LLMClient
llm = LLMClient()

def generate_ic_memo_outline(deal_name: str, doc_text: str) -> dict:
    prompt = f"DEAL:\n{deal_name}\n\nDOC EXCERPT:\n{doc_text[:4000]}\n"
    return llm.complete_json(
        system="You are a private credit IC memo writer. Produce an IC memo outline and key questions.",
        user=prompt,
        schema_name="ICMemoOutline",
    )

def answer_question(doc_text: str, question: str) -> str:
    q = question.lower()
    idx = doc_text.lower().find(q.split(" ")[0])
    if idx == -1:
        return "Demo answer: Relevant section not found; in real mode this is RAG + citations."
    start = max(0, idx-300)
    end = min(len(doc_text), idx+600)
    return f"Found relevant excerpt:\n\n{doc_text[start:end]}"

