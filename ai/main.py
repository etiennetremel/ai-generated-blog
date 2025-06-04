import asyncio
import json
import logfire
import os
import textwrap
from datetime import datetime, timezone
from pydantic_ai.usage import Usage, UsageLimits
from pydantic_ai import UnexpectedModelBehavior, capture_run_messages
from utils import slugify, get_sanitized_model
from director_agent import director_agent


traces_endpoint = "http://localhost:4318/v1/traces"
os.environ["OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"] = traces_endpoint

logfire.configure(
    service_name="ai-generated-blog",
    send_to_logfire=False,
)
logfire.instrument_pydantic_ai()


async def main():
    message_history = None
    usage = Usage()
    usage_limits = UsageLimits(request_limit=20)

    prompt = textwrap.dedent(
        """
        Create a technical blog post.
        - Use the provided editorial guidelines.
        - The audience is technical professionals.
        - Oversee all steps: content writing, editing, SEO, and technical review.
        """
    )

    result = None

    with capture_run_messages() as messages:
        try:
            result = await director_agent.run(
                prompt,
                message_history=message_history,
                usage=usage,
                usage_limits=usage_limits,
            )
        except UnexpectedModelBehavior as e:
            print("An error occurred during agent run (UnexpectedModelBehavior):", e)
            print("cause:", repr(e.__cause__))
            print("messages:", messages)
            raise
        except Exception as e:
            print(
                f"An unexpected error occurred during agent run: {type(e).__name__}: {e}"
            )
            raise

    print("---Final Post---")
    print(result.output)
    print(result.usage())

    # Write the final post to a file
    slug = slugify(result.output.title)
    output_path = os.path.join("../content/posts", f"{slug}.md")
    with open(output_path, "a", encoding="utf-8") as file:
        file.write("+++\n")
        file.write(f"date = '{datetime.now(timezone.utc).isoformat()}'\n")
        file.write(f"title = '{result.output.title}'\n")
        file.write(f"summary = '{result.output.summary}'\n")  # type: ignore
        file.write(f"draft = 'false'\n")
        file.write(f"model = '{get_sanitized_model()}'\n")
        file.write(f"tags = {json.dumps(result.output.tags)}\n")  # type: ignore
        file.write("+++\n\n")
        file.write(result.output.content)  # type: ignore


if __name__ == "__main__":
    asyncio.run(main())
