def score_idea(thesis_tags: list[str], novelty: float, urgency: float) -> float:
    base = min(1.0, 0.2 * len(thesis_tags))
    return round(100 * (0.4*base + 0.3*novelty + 0.3*urgency), 1)

