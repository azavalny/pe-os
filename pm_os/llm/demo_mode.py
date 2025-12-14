import random

def demo_complete_json(*, system: str, user: str, schema_name: str) -> dict:
    seed = abs(hash(user + schema_name)) % (10**6)
    random.seed(seed)

    if schema_name == "RelevanceResult":
        rel = random.choice(["High","Medium","Low"])
        return {
            "relevance": rel,
            "reasons": ["Mentions sector-aligned theme", "Contains new datapoint vs repeated noise"] if rel != "Low" else ["Generic update"],
            "thesis_tags": random.sample(["energy","power","ev","sustainability","grid"], k=2),
            "suggested_crm_updates": {"last_touch": "today", "topic": "market update"}
        }

    if schema_name == "SnippetInsight":
        return {
            "summary": "Condensed summary of the snippet with the one actionable delta.",
            "themes": random.sample(["rates","power prices","ev supply chain","grid capex"], k=2),
            "metrics": {"delta_1w": f"{random.choice(['+','-'])}{round(random.random()*4,2)}%"},
            "thesis_match": random.sample(["power","sustainability","energy"], k=2),
        }

    if schema_name == "DocCompareResult":
        return {
            "high_level_changes": ["Tightened reporting language", "Updated collateral definition"],
            "risk_flags": ["Potential covenant headroom reduced"],
            "covenant_updates": ["Debt/EBITDA test frequency changed to quarterly"]
        }

    if schema_name == "ICMemoOutline":
        return {
            "deal_name": "Demo Deal",
            "sections": ["Executive Summary","Business Overview","Market/Thesis Fit","Key Terms","Downside Case","Risks & Mitigants","Recommendation"],
            "key_risks": ["Customer concentration", "Refinancing risk", "Regulatory risk"],
            "key_questions": ["What changed since last amendment?", "Any covenant step-downs?", "Who are top customers?"]
        }

    return {}

