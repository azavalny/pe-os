from pydantic import BaseModel, Field
from typing import Literal, Optional, List

class RelevanceResult(BaseModel):
    relevance: Literal["High", "Medium", "Low"]
    reasons: List[str] = Field(default_factory=list)
    thesis_tags: List[str] = Field(default_factory=list)
    suggested_crm_updates: dict = Field(default_factory=dict)

class SnippetInsight(BaseModel):
    summary: str
    themes: List[str] = Field(default_factory=list)
    metrics: dict = Field(default_factory=dict)
    thesis_match: List[str] = Field(default_factory=list)

class IdeaCard(BaseModel):
    title: str
    company: str
    thesis_tags: List[str]
    score: float
    next_actions: List[str]

class DocCompareResult(BaseModel):
    high_level_changes: List[str]
    risk_flags: List[str]
    covenant_updates: List[str] = Field(default_factory=list)

class ICMemoOutline(BaseModel):
    deal_name: str
    sections: List[str]
    key_risks: List[str]
    key_questions: List[str]

