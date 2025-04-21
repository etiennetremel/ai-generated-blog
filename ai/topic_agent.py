import os
import re
from typing import Union
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from utils import model, read_file
from inspiration_agent import inspiration_agent, InspirationFailed

instructions = """
You are a technical content strategist at a leading technical publication focused on modern infrastructure and software delivery practices.

<workflow>
1. Use the `get_existing_blog_titles` tool to get a list of existing blog posts titles from the `../content/posts` directory.
2. Use the `get_editorial_guideline` tool to get the editorial guideline from `./editorial-guideline.md`.
3. Use `get_inspiring_topics` to get a list of inspiring topics from top-tier news gathering website RSS feeds, including:
  - https://thenewstack.io/blog/feed/
  - https://techcrunch.com/feed/
4. Generate a single, high-quality blog post topic clearly aligned with the editorial guidelines.
5. You must only return a single field: 'topic'. Do not include anything else.
</workflow>

<rules>
- The topic must NOT overlap or duplicate with the list of existing blog posts titles.
- The topic must match the expertise, be relevant, practical, and timely.
- Ensure topics are applicable to real-world practitioners.
- Align clearly with editorial guidelines:
  - Clear, concise, technical yet accessible language
  - No fluff or hype; real-world practitioner relevance only
  - Suitable specifically for a blog format (avoid whitepapers, tutorials, step-by-step guides, news briefs)
  - Encourage community interest and discussion
  - Topic should be written using sentence case
</rules>
"""


class Topic(BaseModel):
    topic: str


class TopicFailed(BaseModel):
    pass


topic_agent = Agent(
    model,
    result_type=Union[Topic, TopicFailed],  # type: ignore
    instructions=instructions,
)


@topic_agent.tool_plain
async def get_existing_blog_titles(directory: str) -> list[str]:
    titles = []
    for filename in os.listdir(directory):
        if filename == "_index.md":
            continue

        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                match = re.search(r"^\+\+\+\n(.*?)\n\+\+\+", content, re.DOTALL)
                if match:
                    frontmatter = match.group(1)
                    title_match = re.search(
                        r"^title\s*=\s*['\"](.+)['\"]$", frontmatter, re.MULTILINE
                    )
                    if title_match:
                        titles.append(title_match.group(1).strip())

    print("Found existing blog post title(s)", titles)

    return titles


@topic_agent.tool_plain
async def get_editorial_guideline(path: str) -> str:
    print(f'Reading editorial guideline from "{path}"')
    return read_file(path)


@topic_agent.tool
async def get_inspiring_topics(ctx: RunContext[None], url: str) -> list[str]:
    inspiration_result = await inspiration_agent.run(
        url,
        usage=ctx.usage,
    )
    if isinstance(inspiration_result.output, InspirationFailed):
        print("Failed choosing topic")
        print(inspiration_result.output)
        return []

    print(inspiration_result.output)
    print(inspiration_result.usage())
    return inspiration_result.output.topics  # type: ignore
