from typing import TypedDict, List

class ResearchState(TypedDict):
    user_query: str
    clarified_query: str
    brief: str
    draft: str
    feedback: List[str]
    quality_score: float
    approved: bool
    final_report: str
