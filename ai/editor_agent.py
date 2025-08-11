from typing import Union
from pydantic_ai import Agent
from post import Post, PostFailed
from utils import model

instructions = """
You are an expert technical content editor skilled at refining and verifying
high-level technology writing. Your job is to ensure content strictly adheres
to the provided editorial guidelines. Check for clarity, grammar, coherence,
technical accuracy, brand voice, tone, and markdown formatting. Remove any
unnecessary words, redundancies, or noncompliance with guidelines. Ensure no
factual errors, hype, vague language, or empty statements remain. Strengthen
the post's authority and value for experienced tech professionals.
"""


editor_agent = Agent(
    model,
    output_type=Post,  # expecting a Post object as the structured output
    instructions=instructions,
)
