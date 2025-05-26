import os
import re
import feedparser
import frontmatter
from typing import Any
from functools import lru_cache

model = os.getenv("MODEL", "openai:gpt-4.1")


def get_sanitized_model():
    """
    Return correct model based on Pydantic configuration
    In the case of Grok, the xAI API is compatible with the OpenAI API which
    Pydantic is using. so openai:grok-3 would become xai:grok-3.
    Similarly, if using OpenRouter, strip the openrouter: from the model name.
    """

    # OpenRouter
    if "/" in model:
        s = model
        if "meta-llama/" in s:
            s = model.replace("meta-llama", "meta")
        return model[model.find(":") + 1 :].replace("/", ":")

    # Grok
    if "grok" in model:
        return model.replace("openai", "xai")

    return model


@lru_cache(maxsize=None)
def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def slugify(name):
    filename = name.lower()
    filename = re.sub(r"[^a-z0-9]+", " ", filename)
    filename = re.sub(r"\s+", "-", filename.strip())
    return filename


@lru_cache(maxsize=None)
def _get_blog_post_metadata(filepath: str) -> Any:
    """
    Return blog post metadata from provided filepath
    """
    return frontmatter.load(filepath)


@lru_cache(maxsize=None)
def _get_blog_post_paths(directory: str) -> list[str]:
    """
    Return list of blog post paths from provided directory
    """
    paths = []

    for filename in os.listdir(directory):
        if filename == "_index.md":
            continue

        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            paths.append(filepath)

    return paths


@lru_cache(maxsize=None)
def _get_all_metadata_by_key(directory: str, key: str) -> list[str]:
    """
    Walk through all files from directory, load frontmatter metadata and return
    list of merged values
    """
    output = []
    paths = _get_blog_post_paths(directory)
    for path in paths:
        metadata = _get_blog_post_metadata(path)
        if key in metadata:
            output.append(metadata[key])
    return output


def load_blog_titles(directory: str) -> list[str]:
    """
    Return list of titles from all posts located in provided directory
    """
    titles = _get_all_metadata_by_key(directory, "title")
    return titles


@lru_cache(maxsize=None)
def load_blog_tags(directory: str) -> list[str]:
    """
    Return list of tags from all posts located in provided directory
    """
    tags = []
    metadata_tags = _get_all_metadata_by_key(directory, "tags")
    for tag_list in metadata_tags:
        for tag in tag_list:
            if tag not in tags:
                tags.append(tag)
    return tags


@lru_cache(maxsize=None)
def load_rss_feed_titles(url: str) -> list[str]:
    feed = feedparser.parse(url)
    titles = []
    for entry in feed.entries:
        titles.append(entry.title)

    return titles
