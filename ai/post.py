from pydantic import BaseModel, Field


class Post(BaseModel):
    title: str = Field(description="Title of the blog post, max 20 words")
    content: str = Field(
        description="Content of the blog post in markdown format without the main title, max 2000 words"
    )
    summary: str = Field(
        description="Concise, compelling Summary of the blog post, max 35 words"
    )
    tags: list[str] = Field(
        description="List of relevant tags for the blog post, max 3 tags"
    )


class PostFailed(BaseModel):
    pass
