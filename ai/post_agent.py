from typing import Union
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from utils import model, load_blog_tags, read_file

instructions = """
You are a professional technical content writer for a news-gathering company.

Your responsibilities:
- Write engaging, technically accurate, and factual blog posts.
- Clearly adhere to provided editorial guidelines at all times.
- Match content precisely to brand brief (voice, tone, values, audience).
- Deliver content strictly formatted as defined below.
- Always produce content ready for immediate review.
- Ensure the content strictly meets all editorial guidelines and aligns with brand tone and voice.

<workflow>
1. Retrieve editorial guidelines using `get_editorial_guideline` tool from `./editorial-guideline.md`.
2. Write a complete, accurate, high-quality blog post strictly following the retrieved editorial guidelines.
3. Retrieve all existing tags using the `get_existing_tags` tool from the `../content/posts` directory.
   - Reuse existing tags if directly relevant to the content.
   - If no existing tags adequately match the content, create new, precise tags.
4. Clearly return your response with these exact fields:
   - title: concise and engaging post title (sentence case).
   - post: full blog post content in markdown format.
   - summary: concise summary of the blog post (maximum 35 words).
   - tags: relevant list of tags for categorizing the post.
</workflow>
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
    instructions=instructions,
)


@post_agent.tool_plain
async def get_editorial_guideline(path: str) -> str:
    return read_file(path)


@post_agent.tool_plain
async def get_existing_tags(directory: str) -> list[str]:
    return load_blog_tags(directory)
