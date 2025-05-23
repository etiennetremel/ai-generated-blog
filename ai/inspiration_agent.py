from typing import Union
from pydantic import BaseModel
from pydantic_ai import Agent
from utils import load_rss_feed_titles, model, read_file

instructions = """
You're a bot that scrapes RSS feeds to find the best inspirational blog post topics.

Your responsibilities:
- Scrape and analyze RSS feeds.
- Evaluate blog post titles against the brand brief criteria (voice, audience, tone, themes, and values).
- Curate inspirational topic ideas that align closely with the brand and editorial guidelines.

<workflow>
1. Evaluate each title from provided RSS feed URL against the editorial guideline located at `./editorial-guideline.md`
2. Select and return only the 10 most inspiring, relevant, and actionable topics.
</workflow>
"""


class Inspiration(BaseModel):
    topics: list[str]


class InspirationFailed(BaseModel):
    pass


inspiration_agent = Agent(
    model,
    result_type=Union[Inspiration, InspirationFailed],  # type: ignore
    instructions=instructions,
)


@inspiration_agent.tool_plain
async def get_titles(url: str) -> list[str]:
    return load_rss_feed_titles(url)


@inspiration_agent.tool_plain
async def get_editorial_guideline(path: str) -> str:
    return read_file(path)
