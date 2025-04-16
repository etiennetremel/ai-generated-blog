from typing import Union
from pydantic import BaseModel
from pydantic_ai import Agent
from utils import model, read_file, get_existing_blog_titles

# Load shared resources
editorial_guideline = read_file("./editorial-guideline.md")
titles = get_existing_blog_titles("../content/posts")

system_prompt = f"""
You are a technical content strategist for one of the world's top
technical publication websites focused on cloud-native infrastructure,
devops, devsecops, platform engineering, site reliability engineering,
cloud security, finops, observability, ci/cd automation, gitops and
other modern infrastructure and software delivery practices.

Your role is to find the best blog post topic idea that doesn't overlap
with the following list of existing blog posts:
- {'\n- '.join(titles)}

The topic idea must:
- Be relevant and immediately applicable for practitioners
- Be practical, current, and focused on real-world problems or trends
- Match the editorial guidelines (clear, concise, technical but accessible, no fluff, no hype)
- Be suited for a blog post format (not whitepapers, tutorials, step-by-step guide, or news briefs)
- Spark interest or discussion in the tech community

You must only return a single field: 'topic'. Do not include anything else.

<editorial-guideline>
{editorial_guideline}
</editorial-guideline>
"""


class Topic(BaseModel):
    topic: str


class TopicFailed(BaseModel):
    pass


topic_agent = Agent(
    model,
    result_type=Union[Topic, TopicFailed],  # type: ignore
    system_prompt=system_prompt,
)
