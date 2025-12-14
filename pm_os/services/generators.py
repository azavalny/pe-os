def generate_weekly_brief(themes: list[str], top_items: list[dict]) -> str:
    bullets = "\n".join([f"- {x['title']}: {x.get('summary','')}" for x in top_items[:5]])
    return f"Top themes: {', '.join(themes[:5])}\n\nTop items:\n{bullets}"

