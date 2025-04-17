import os
import re

model = os.getenv("MODEL", "openai:gpt-4.1")


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
