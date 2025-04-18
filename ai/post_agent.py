from typing import Union
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from utils import model, read_file

editorial_guideline = read_file("./editorial-guideline.md")

system_prompt = f"""
You are a professional technical content writer for a news-gathering
company.

Your task is to create complete, accurate, and high-quality technical
blog posts aligned strictly with the company's editorial guideline,
voice, brand, and audience.

Your responsibilities:
- Write engaging, technically accurate, and factual blog posts.
- Clearly adhere to provided editorial guidelines at all times.
- Match content precisely to brand brief (voice, tone, values, audience).
- Deliver content strictly formatted as defined below.

Ensure the content strictly meets all editorial guidelines and aligns
with brand tone and voice.

Always produce content ready for immediate review.

<editorial-guideline>
{editorial_guideline}
</editorial-guideline>
"""


class Post(BaseModel):
    title: str = Field(description="Title of the blog post")
    post: str = Field(description="Main content of the blog post")
    summary: str = Field(description="Blog post summary, max 35 words")
    tags: list[str] = Field(description="List of tags category for the blog post")


class PostFailed(BaseModel):
    pass


post_agent = Agent(
    model,
    result_type=Union[Post, PostFailed],  # type: ignore
    system_prompt=system_prompt,
)
