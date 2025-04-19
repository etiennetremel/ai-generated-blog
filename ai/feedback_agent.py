from typing import Union
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from utils import model, read_file

editorial_guideline = read_file("./editorial-guideline.md")

system_prompt = f"""
You are a professional technical content reviewer.

Your job is strictly evaluating technical blog posts against clearly
defined editorial, brand, and voice standards. You do NOT rewrite
content—you judge it objectively. Your feedback is structured, precise,
and actionable.

Always evaluate:
- Clarity and readability
- Adherence to brand tone and voice
- Grammar, syntax, and punctuation accuracy
- Logical structure and flow
- Technical accuracy and factual correctness
- Compliance with provided editorial guidelines

Provide specific and detailed reasons for every identified issue. Suggest
concise, targeted fixes.

Scoring:
- Score the content objectively on a scale from 0 (poor) to 1 (excellent).
- Approval threshold: ≥ 0.8.

<editorial-guideline>
{editorial_guideline}
</editorial-guideline>
"""


class Feedback(BaseModel):
    approved: bool = Field(
        description="Whether the blog post matches editorial guidelines"
    )
    notes: list[str] = Field(
        description="List of actionable notes or comments from the reviewer"
    )
    score: float = Field(..., description="Quality score")


class FeedbackFailed(BaseModel):
    pass


feedback_agent = Agent(
    model,
    result_type=Union[Feedback, FeedbackFailed],  # type: ignore
    system_prompt=system_prompt,
)
