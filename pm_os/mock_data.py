import pandas as pd
from pm_os.db import SessionLocal
from pm_os.models import Company, Deal, Email, MarketSnippet, Document, Covenant

def seed_from_csv():
    db = SessionLocal()

    def load(path): return pd.read_csv(path)

    companies = load("data/seed/companies.csv")
    for _, r in companies.iterrows():
        db.add(Company(name=r["name"], sector=r["sector"], tags=r.get("tags","")))

    db.commit()

    deals = load("data/seed/deals.csv")
    for _, r in deals.iterrows():
        db.add(Deal(company_id=int(r["company_id"]), deal_type=r["deal_type"], stage=r["stage"],
                    thesis_tags=r.get("thesis_tags",""), score=float(r.get("score",0)), owner=r.get("owner","")))

    emails = load("data/seed/emails.csv")
    for _, r in emails.iterrows():
        db.add(Email(sender=r["sender"], subject=r["subject"], body=r["body"]))

    snippets = load("data/seed/market_snippets.csv")
    for _, r in snippets.iterrows():
        db.add(MarketSnippet(source=r["source"], title=r["title"], text=r["text"]))

    docs = load("data/seed/documents.csv")
    for _, r in docs.iterrows():
        db.add(Document(deal_id=int(r["deal_id"]), doc_type=r["doc_type"], version=r["version"], text=r["text"]))

    covs = load("data/seed/covenants.csv")
    for _, r in covs.iterrows():
        db.add(Covenant(deal_id=int(r["deal_id"]), covenant_type=r["covenant_type"], threshold=r["threshold"],
                        test_frequency=r["test_frequency"], next_due_date=r["next_due_date"], source_note=r.get("source_note","")))

    db.commit()
    db.close()

