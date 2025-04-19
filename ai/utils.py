import os
import re

model = os.getenv("MODEL", "openai:gpt-4.1")


def get_sanitized_model():
    """
    Return correct model based on Pydantic configuration
    In the case of Grok, the xAI API is compatible with the OpenAI API which
    Pydantic is using. so openai:grok-3 would become xai:grok-3
    """
    if "grok" in model:
        return model.replace("openai", "xai")
    return model


def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def slugify(name):
    filename = name.lower()
    filename = re.sub(r"[^a-z0-9]+", " ", filename)
    filename = re.sub(r"\s+", "-", filename.strip())
    return filename


def get_existing_blog_titles(directory):
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
    return titles
