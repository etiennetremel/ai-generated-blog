import textwrap
from editor_agent import editor_agent
from post import Post, PostFailed
from pydantic_ai import Agent, RunContext, ModelRetry
from seo_agent import seo_agent
from tech_lead_agent import tech_lead_agent
from typing import Union
from utils import (
    load_blog_titles,
    load_blog_tags,
    load_rss_feed_titles,
    model,
    read_file,
)
from writer_agent import writer_agent

editorial_guideline = read_file("./editorial-guideline.md")
hugo_posts_directory = "../content/posts"

instructions = """
You are a director of an AI agent orchestrator for producing high-quality
technical blog posts. Your workflow coordinates a pipeline where each
specialist agent and tools are called at the appropriate stage. Available tools
include:

- writer: technical content writer
- editor: technical content editor
- seo: SEO specialist
- tech lead: experienced technology lead
- get_rss_feed_titles: retrieves a list of blog post titles from a provided RSS
  feed URL, for inspiration when crafting a unique title
- get_existing_titles: retrieves a list of currently published blog titles to
  ensure title uniqueness
- get_existing_tags: retrieves a list of currently published blog tags to
  ensure re-using tags when possible


# Responsibilities:

- Enforce the provided editorial guidelines, ensuring all outputs meet brand
  identity, audience, and technical standards.
- Sequence the pipeline: writer → editor → seo → tech lead, calling title/tools
  as needed.
- Always guide each agent with clear instructions and relevant context at each
  step.
- If a blog title isn't provided by the user, generate a unique title that does
  not overlap with existing titles. For inspiration, fetch titles from RSS
  feeds such as:
    - https://thenewstack.io/blog/feed/
    - https://www.cncf.io/blog/feed/
    - https://devops.com/feed/
- Use get_existing_titles to check for uniqueness before finalizing.
- Use get_existing_tags to check if a similar tag already exist and use it
  otherwise come up with your own more relevant tags before finalizing.
- Output format must be:
    - Title: string (unique, high quality, ≤ 120 characters)
    - Content: markdown-formatted blog post (≤ 120 characters per line)
    - Tags: list of up to 3 relevant tags
    - Summary: concise, compelling overview (≤ 35 words)
- Do NOT include any explanations or extra text.
- Only deliver the final, fully reviewed and edited post.
- Rigorously monitor compliance, clarity, technical correctness, and
  professional value at every stage. Refine outputs as needed.
- All communication to tools and in content should follow user-facing language
  (simple, direct, non-robotic).
"""


director_agent = Agent(
    model,
    result_type=Union[Post, PostFailed],  # type: ignore
    instructions=instructions,
)


@director_agent.tool_plain
async def get_existing_titles() -> list[str]:
    """Retrieve the list of existing blog post titles of this project"""
    print("Calling get_existing_titles")
    return load_blog_titles(hugo_posts_directory)


@director_agent.tool_plain
async def get_existing_tags() -> list[str]:
    """Retrieve the list of existing blog post tags of this project"""
    print("Calling get_existing_tags")
    return load_blog_tags(hugo_posts_directory)


@director_agent.tool_plain
async def get_rss_feed_titles(url: str) -> list[str]:
    """Retrieve a list of blog post titles from a given RSS feed URL"""
    print(f"Calling get_rss_feed_titles {url}")
    return load_rss_feed_titles(url)


@director_agent.tool(retries=3)
async def writer(ctx: RunContext[None], topic: str) -> Post:
    """A professional technical content writer"""
    print("Calling Writer")
    result = await writer_agent.run(
        textwrap.dedent(
            """
            Please create a comprehensive technical blog post covering the
            provided topic: {topic}.

            Follow the editorial guidelines.

            - Ensure technical accuracy, practical insights, and clear structure.
            - Write like a practitioner for practitioners.
            - Use markdown formatting as specified.
            - Avoid all listed "Do nots."
            - Output format must be:
                - Title: string (unique, high quality, ≤ 120 characters)
                - Content: markdown-formatted blog post (≤ 120 characters per line)
                - Tags: list of up to 3 relevant tags
                - Summary: concise, compelling overview (≤ 35 words)
            - Do NOT include any explanations or extra text.

            <editorial_guideline>
            {editorial_guideline}
            </editorial_guideline>
            """
        ).format(
            topic=topic,
            editorial_guideline=editorial_guideline,
        ),
        deps=ctx.deps,
        usage=ctx.usage,
    )
    print("writer result:", result)

    if result.output is None:
        raise ModelRetry(f"No result returned")

    return result.output  # type: ignore


@director_agent.tool(retries=3)
async def editor(ctx: RunContext[None], post: Post) -> Post:
    """A professional technical content editor"""
    print("Calling Editor")
    result = await editor_agent.run(
        textwrap.dedent(
            """
            Please review and edit the following content for strict compliance
            with our editorial guidelines.

            - Identify and rewrite unclear, wordy, or off-brand passages.
            - Fix factual, stylistic, or formatting mistakes.
            - Ensure concise, insightful, and practical analysis.
            - Output format must be:
                - Title: string (unique, high quality, ≤ 120 characters)
                - Content: markdown-formatted blog post (≤ 120 characters per line)
                - Tags: list of up to 3 relevant tags
                - Summary: concise, compelling overview (≤ 35 words)
            - Do NOT include any explanations or extra text.

            <post>
            {post}
            </post>

            <editorial_guideline>
            {editorial_guideline}
            </editorial_guideline>
            """
        ).format(
            post=post,
            editorial_guideline=editorial_guideline,
        ),
        deps=ctx.deps,
        usage=ctx.usage,
    )

    if result.output is None:
        raise ModelRetry(f"No result returned")

    return result.output  # type: ignore


@director_agent.tool(retries=3)
async def seo(ctx: RunContext[None], post: Post) -> Post:
    """A professional SEO specialist"""
    print("Calling SEO")
    result = await seo_agent.run(
        textwrap.dedent(
            """
            Analyze and optimize the following technical blog post for SEO best
            practices, ensuring all editorial guidelines are followed.

            - Suggest effective, naturally integrated keywords.
            - Adjust headings and tags where needed.
            - Ensure meta data is concise and compelling.
            - Do not compromise clarity or credibility.
            - Output format must be:
                - Title: string (unique, high quality, ≤ 120 characters)
                - Content: markdown-formatted blog post (≤ 120 characters per line)
                - Tags: list of up to 3 relevant tags
                - Summary: concise, compelling overview (≤ 35 words)
            - Do NOT include any explanations or extra text.

            <post>
            {post}
            </post>

            <editorial_guideline>
            {editorial_guideline}
            </editorial_guideline>
            """
        ).format(
            post=post,
            editorial_guideline=editorial_guideline,
        ),
        deps=ctx.deps,
        usage=ctx.usage,
    )

    if result.output is None:
        raise ModelRetry(f"No result returned")

    return result.output  # type: ignore


@director_agent.tool(retries=3)
async def tech_lead(ctx: RunContext[None], post: Post) -> Post:
    """A professional technical lead"""
    print("Calling Teach Lead")
    result = await tech_lead_agent.run(
        textwrap.dedent(
            """
            Review this technical blog post for technical correctness, depth,
            and compliance with our editorial guidelines.

            - Note and correct any technical inaccuracies, unclear
              explanations, or missing best practices.
            - Enhance with brief, high-impact practical examples if missing.
            - Verify citation of sources or standards.
            - Output format must be:
                - Title: string (unique, high quality, ≤ 120 characters)
                - Content: markdown-formatted blog post (≤ 120 characters per line)
                - Tags: list of up to 3 relevant tags
                - Summary: concise, compelling overview (≤ 35 words)
            - Do NOT include any explanations or extra text.

            <post>
            {post}
            </post>

            <editorial_guideline>
            {editorial_guideline}
            </editorial_guideline>
            """
        ).format(
            post=post,
            editorial_guideline=editorial_guideline,
        ),
        deps=ctx.deps,
        usage=ctx.usage,
    )

    if result.output is None:
        raise ModelRetry(f"No result returned")

    return result.output  # type: ignore
