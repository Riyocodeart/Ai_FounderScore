from pydantic import BaseModel

class StartupInput(BaseModel):
    idea_description: str
    target_market: str
    revenue_model: str
    estimated_budget: float