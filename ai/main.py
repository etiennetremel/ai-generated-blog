import asyncio
import json
import os
import textwrap
from datetime import datetime, timezone
from pydantic_ai.usage import Usage, UsageLimits
from utils import slugify, get_sanitized_model
from topic_agent import topic_agent, TopicFailed
from feedback_agent import feedback_agent, FeedbackFailed
from post_agent import post_agent, PostFailed


async def main():
    message_history = None
    usage = Usage()
    usage_limits = UsageLimits(request_limit=20)

    # Choose a topic
    topic_result = await topic_agent.run(
        "Give me a relevant topic",
        message_history=message_history,
        usage=usage,
        usage_limits=usage_limits,
    )
    if isinstance(topic_result.output, TopicFailed):
        print("Failed choosing topic")
        print(topic_result.output)
        return

    print(topic_result.output)
    print(topic_result.usage())

    # Generate a blog post based on the topic
    post_user_prompt = textwrap.dedent(
        """
        Write a complete, publication-ready blog post about the following
        topic:

        "{topic}"

        # Clearly structure your response as follows:
        - **title:** Concise, descriptive, engaging.
        - **summary:** A short, clear, and informative summary (35 words max).
        - **blog_post:** Complete blog content formatted in markdown (follows
        editorial guidelines, DOT NOT include the post title within the
        content).
        - **tags:** Relevant keywords or phrases (3–6 tags max, lowercase, no
        hashtags, separated by commas).
        """
    ).format(
        topic=topic_result.output.topic  # type: ignore
    )

    post_result = await post_agent.run(
        post_user_prompt,
        message_history=message_history,
        usage=usage,
        usage_limits=usage_limits,
    )
    if post_result.output.__class__.__name__ == "PostFailed":
        print("Failed creating post")
        print(post_result)
        return

    print(post_result.output)
    print(post_result.usage())

    # Get editorial feedback and revise as needed
    attempts = 1
    while True:
        feedback_user_prompt = textwrap.dedent(
            """
            Review the provided blog post content against the Writing Criteria and Editorial Guidelines.

            # Structured Review Workflow

            ## Step 1: Editorial Evaluation

            Check the content carefully against these criteria:
            - Clarity: Is the writing clear and easy to follow?
            - Tone: Does the tone match the brand brief?
            - Grammar and Syntax: Are grammar, punctuation, and wording correct and natural?
            - Structure: Does the content have logical flow, clear sections, and effective headings?
            - Technical and Factual Accuracy: Is the information correct and reliable?
            - Brand Alignment: Does the writing fit the brand’s voice, audience, values, and themes?

            For each issue you find:
            - Identify it specifically.
            - Explain the problem in one or two plain sentences.
            - Suggest one or two focused, actionable improvements (no vague feedback).

            If there are no issues in a category, explicitly state that.

            ## Step 2: Scoring (0–1 Scale)

            Assign a score based on the following:

            | Score Range | Meaning | Action
            |-------------|---------|----------|
            | 0–0.49 | Major problems; content needs major rewriting | Reject and list required critical fixes
            | 0.5–0.79 | Moderate problems; revisions needed before publishing | Reject and provide clear, specific improvements
            | 0.8–0.89 | Good quality; minor optional edits only | Approve and suggest optional polish
            | 0.9–1.0 | Excellent; publish as-is, only very light optional polish | Approve

            Important:
            - Avoid defaulting to the middle range (0.5–0.79).
            - Be decisive: if the content feels solid with only light tweaks, score above 0.8.
            - If you find even moderate issues, score below 0.8.
            - Base the score purely on the quality, not effort or intention.

            <post>
            {post}
            </post>
            """
        ).format(
            post=post_result.output.post  # type: ignore
        )

        feedback_result = await feedback_agent.run(
            feedback_user_prompt,
            message_history=message_history,
            usage=usage,
            usage_limits=usage_limits,
        )
        if isinstance(feedback_result.output, FeedbackFailed):
            print("Failed providing feedback")
            return

        print(f"[{attempts}]", feedback_result.output)
        print(feedback_result.usage())

        if feedback_result.output.approved:  # type: ignore
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
            """
        ).format(
            feedback=feedback_result.output.notes,  # type: ignore
            post=post_result.output.post,  # type: ignore
        )

        post_result = await post_agent.run(
            revision_user_prompt,
            message_history=message_history,
            usage=usage,
            usage_limits=usage_limits,
        )
        if isinstance(post_result.output, PostFailed):
            print("Failed revisiting post")
            return

        attempts += 1

    print("---Final Post---")
    print(post_result.output)
    print(post_result.usage())

    # Write the final post to a file
    slug = slugify(post_result.output.title)
    output_path = os.path.join("../content/posts", f"{slug}.md")
    with open(output_path, "a", encoding="utf-8") as file:
        file.write("+++\n")
        file.write(f"date = '{datetime.now(timezone.utc).isoformat()}'\n")
        file.write(f"title = '{post_result.output.title}'\n")
        file.write(f"summary = '{post_result.output.summary}'\n")  # type: ignore
        file.write(f"draft = 'false'\n")
        file.write(f"model = '{get_sanitized_model()}'\n")
        file.write(f"tags = {json.dumps(post_result.output.tags)}\n")  # type: ignore
        file.write("+++\n\n")
        file.write(post_result.output.post)  # type: ignore


if __name__ == "__main__":
    asyncio.run(main())
