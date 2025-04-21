from typing import Union
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from utils import model, read_file

instructions = """
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

<workflow>
1. Use the `get_editorial_guideline` tool to get the editorial guideline from `./editorial-guideline.md`.
2. Evaluate blog posts againts editorial guideline.
3. Score and provide specific and detailed reasons for every identified issue. Suggest concise, targeted fixes.
</workflow>

<scoring>
- Score the content objectively on a scale from 0 (poor) to 1 (excellent).
- Approval threshold: ≥ 0.8.
</scoring>
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
    instructions=instructions,
)


@feedback_agent.tool_plain
async def get_editorial_guideline(path: str) -> str:
    return read_file(path)
