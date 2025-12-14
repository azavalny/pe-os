THEME_KEYWORDS = {
    "energy": ["oil","gas","energy","upstream","midstream"],
    "power": ["power","grid","utility","electricity","iso","transmission"],
    "ev": ["ev","battery","charging","lithium"],
    "sustainability": ["sustain","renewable","solar","wind","carbon","esg"],
    "rates": ["rates","yield","treasury","inflation"],
}

def tag_text(text: str) -> list[str]:
    t = text.lower()
    tags = []
    for tag, kws in THEME_KEYWORDS.items():
        if any(k in t for k in kws):
            tags.append(tag)
    return tags[:5]

