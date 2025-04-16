import asyncio
import json
import os
import textwrap
from datetime import datetime, timezone
from pydantic_ai.usage import Usage, UsageLimits
from utils import read_file, slugify
from topic_agent import topic_agent
from feedback_agent import feedback_agent
from post_agent import post_agent


async def main():
    message_history = None
    usage = Usage()
    usage_limits = UsageLimits(request_limit=20)
    editorial_guideline = read_file("./editorial-guideline.md")

    # Choose a topic
    topic_result = await topic_agent.run(
        message_history=message_history,
        usage=usage,
        usage_limits=usage_limits,
    )
    if topic_result.data.__class__.__name__ == "TopicFailed":
        print("Failed choosing topic")
        print(topic_result.data)
        return

    print(topic_result.data)
    print(topic_result.usage())

    # Generate a blog post based on the topic
    post_user_prompt = textwrap.dedent(
        """
        Write a complete, publication-ready blog post about the following
        topic:

        "{topic}"

        # Clearly structure your response as follows:
        - **Title:** Clearly written in sentence case, concise, engaging.
        - **Summary:** Clear, informative summary of the main points (35 words max).
        - **Blog_post:** Complete blog content clearly formatted in markdown,
          adhering fully to editorial guidelines.
        - **Tags:** 3–6 relevant tags, lowercase, comma-separated, no hashtags.

        Ensure the content strictly meets all editorial guidelines and aligns
        with brand tone and voice.
        """
    ).format(
        topic=topic_result.data.topic  # type: ignore
    )

    post_result = await post_agent.run(
        post_user_prompt,
        message_history=message_history,
        usage=usage,
        usage_limits=usage_limits,
    )
    if post_result.data.__class__.__name__ == "PostFailed":
        print("Failed creating post")
        print(post_result)
        return

    print(post_result.data)
    print(post_result.usage())

    # Get editorial feedback and revise as needed
    attempts = 1
    while True:
        feedback_user_prompt = textwrap.dedent(
            """
            Review the provided blog post content against the Writing Criteria and Editorial Guidelines.

            # Structured Review Workflow

            ## Step 1: Evaluate against editorial guidelines
            Carefully check the content for compliance with:
            - Clarity (clear and easy to follow)
            - Tone (matches brand brief)
            - Grammar and syntax (clean and correct)
            - Structure (logical flow, clear sections, effective headings)
            - Technical and factual accuracy (content correctness, no misleading information)
            - Adherence to brand brief (voice, audience, values, themes)

            Clearly log each violation:
            - Identify specific issues
            - Explain the issue briefly and plainly
            - Suggest targeted, actionable improvements (keep suggestions short and practical)

            ## Step 2: Assign a numeric quality score (0–1)
            Use this rubric to assign your numeric score:

            | Score Range | Definition                             | Action                     |
            |-------------|----------------------------------------|----------------------------|
            | 0–0.49      | Major revisions required; critical issues | Reject, detailed fixes      |
            | 0.5–0.79    | Minor-to-moderate issues; revisions necessary | Reject, clear improvements  |
            | 0.8–0.89    | Good quality, minor optional improvements | Approve, suggest optional polish |
            | 0.9–1.0     | Excellent; ready for immediate publication | Approve, optional minor polish only |

            <post>
            {post}
            </post>
            """
        ).format(
            post=post_result.data.post  # type: ignore
        )

        editorial_feedback_result = await feedback_agent.run(
            feedback_user_prompt,
            message_history=message_history,
            usage=usage,
            usage_limits=usage_limits,
        )
        if (
            editorial_feedback_result.data.__class__.__name__
            == "EditorialFeedbackFailed"
        ):
            print("Failed providing feedback")
            return

        print(f"[{attempts}]", editorial_feedback_result.data)
        print(editorial_feedback_result.usage())

        if editorial_feedback_result.data.approved:  # type: ignore
            break

        revision_user_prompt = textwrap.dedent(
            """
            The previously submitted blog post has been reviewed. Clearly
            incorporate all provided review feedback into your revision.

            - Revise the blog post strictly following editorial guidelines and brand voice.
            - Clearly address each specific issue mentioned in the feedback.
            - Do NOT skip or overlook any feedback points.

            After revision, provide:
            - **Title:** Clearly written in sentence case, concise, engaging.
            - **Summary:** Updated summary reflecting revisions made (1–3 sentences).
            - **Blog_post:** Revised, complete blog content formatted in markdown.
            - **Tags:** Updated relevant tags if necessary (3–6 tags, lowercase, comma-separated).

            <feedback>
            {feedback}
            </feedback>

            <post>
            {post}
            </post>

            <editorial-guideline>
            {editorial_guideline}
            </editorial-guideline>
            """
        ).format(
            feedback=editorial_feedback_result.data.notes,  # type: ignore
            post=post_result.data.post,  # type: ignore
            editorial_guideline=editorial_guideline,
        )

        post_result = await post_agent.run(
            revision_user_prompt,
            message_history=message_history,
            usage=usage,
            usage_limits=usage_limits,
        )
        if post_result.data.__class__.__name__ == "PostFailed":
            print("Failed revisiting post")
            return

        attempts += 1

    print("---Final Post---")
    print(post_result.data)
    print(post_result.usage())

    # Write the final post to a file
    slug = slugify(post_result.data.title)
    output_path = os.path.join("../content/posts", f"{slug}.md")
    with open(output_path, "a", encoding="utf-8") as file:
        file.write("+++\n")
        file.write(f"date = '{datetime.now(timezone.utc).isoformat()}'\n")
        file.write(f"title = '{post_result.data.title}'\n")
        file.write(f"summary = '{post_result.data.summary}'\n")  # type: ignore
        file.write(f"draft = 'false'\n")
        file.write(f"model = '{os.getenv('MODEL', 'openai:gpt-4.1')}'\n")
        file.write(f"tags = {json.dumps(post_result.data.tags)}\n")  # type: ignore
        file.write("+++\n\n")
        file.write(post_result.data.post)  # type: ignore


if __name__ == "__main__":
    asyncio.run(main())
