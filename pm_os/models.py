from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Float, DateTime, Text, ForeignKey
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    sector: Mapped[str] = mapped_column(String(100))
    tags: Mapped[str] = mapped_column(String(500), default="")

class Deal(Base):
    __tablename__ = "deals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    deal_type: Mapped[str] = mapped_column(String(20))
    stage: Mapped[str] = mapped_column(String(50))
    thesis_tags: Mapped[str] = mapped_column(String(500), default="")
    score: Mapped[float] = mapped_column(Float, default=0.0)
    owner: Mapped[str] = mapped_column(String(80), default="")

class Email(Base):
    __tablename__ = "emails"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender: Mapped[str] = mapped_column(String(200))
    subject: Mapped[str] = mapped_column(String(300))
    body: Mapped[str] = mapped_column(Text)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    tags: Mapped[str] = mapped_column(String(500), default="")
    linked_deal_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    linked_lp_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

class MarketSnippet(Base):
    __tablename__ = "market_snippets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(300))
    text: Mapped[str] = mapped_column(Text)
    published_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    tags: Mapped[str] = mapped_column(String(500), default="")

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deal_id: Mapped[int] = mapped_column(Integer)
    doc_type: Mapped[str] = mapped_column(String(60))
    version: Mapped[str] = mapped_column(String(40))
    text: Mapped[str] = mapped_column(Text)

class Covenant(Base):
    __tablename__ = "covenants"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deal_id: Mapped[int] = mapped_column(Integer)
    covenant_type: Mapped[str] = mapped_column(String(80))
    threshold: Mapped[str] = mapped_column(String(80))
    test_frequency: Mapped[str] = mapped_column(String(40))
    next_due_date: Mapped[str] = mapped_column(String(20))
    source_note: Mapped[str] = mapped_column(String(200), default="")

