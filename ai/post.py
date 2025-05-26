from pydantic import BaseModel, Field


class Post(BaseModel):
    title: str = Field(description="Title of the blog post")
    content: str = Field(description="Content of the blog post")
    summary: str = Field(description="Summary of the blog post, max 35 words")
    tags: list[str] = Field(description="List of tags category for the blog post")


class PostFailed(BaseModel):
    pass
