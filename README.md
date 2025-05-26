# AI generated blog

[![Netlify Status](https://api.netlify.com/api/v1/badges/1a34df76-38de-42a1-8bcc-074f144a4b83/deploy-status)](https://app.netlify.com/sites/ai-generated-tech-blog/deploys)

This repository demonstrate how to use [Pydantic AI][pydantic-ai] with
[Hugo][hugo] to generate blog posts on a given topic using different models
(OpenAI GPT 4o, GPT 4.1, o3, Google Gemini 2.5, xAI Grok 2, Grok 3, etc).

> [!WARNING]
>  This project is not intended to flood the web with low-quality AI-generated
>  content. The goal is to explore and demonstrate how different AI models can
>  assist in generating blog posts. Use this responsibly and with a focus on
>  transparency, originality, and value.

## Overview

The diagram below outlines the end-to-end workflow for generating blog posts.

```mermaid
flowchart TD
    Start[Start]
    Topic(((Topic Agent)))
    Inspiration(((Inspiration Agent)))
    Post(((Post Agent)))
    Feedback(((Feedback Agent)))
    QualityCondition{Quality score > 0.8 ?}
    EditorialGuideline@{ shape: doc, label: "Editorial guideline" }
    Publish[Publish post]
    End[End]
    ExistingBlogPostsTitles@{ shape: doc, label: "Existing blog posts titles" }
    ExistingBlogPostsTags@{ shape: doc, label: "Existing blog posts tags" }
    TNS@{ shape: text, label: "thenewstack.io/blog/feed"}
    DO@{ shape: text, label: "devops.com/feed"}
    CNCF@{ shape: text, label: "cncf.io/blog/feed"}

    Start ==> Topic
    Topic -.-> EditorialGuideline
    Topic -. Retrieve post title<br>from file system .-> ExistingBlogPostsTitles
    Topic ==> Inspiration
    Inspiration -.-> EditorialGuideline
    Inspiration -. Fetch RSS feed .-> TNS
    Inspiration -. Fetch RSS feed .-> DO
    Inspiration -. Fetch RSS feed .-> CNCF
    Topic == Generate topic that doesn't<br>overlap with existing posts ==> Post
    Post == Draft post ==> Feedback
    Post -.-> EditorialGuideline
    Post -. Retrieve existing post tags<br>from file system<br>attempt grouping with existing .-> ExistingBlogPostsTags
    Feedback -.-> EditorialGuideline
    Feedback ==> QualityCondition
    QualityCondition == Yes, format post<br>with metadata ==> Publish
    QualityCondition -- No, provide feedback and<br>ask to revisit --> Post
    Publish ==> End
```

## Generating blog posts

To generate a new blog post, choose a model and execute the commands below from
the `./ai/` directory.

Refer to the [Pydantic AI models documentation][pydantic-models] for
instructions to use other models.

### OpenAI

```bash
export OPENAI_API_KEY=your-api-key
export MODEL=openai:gpt-4.1

python main.py
```

### Google Gemini

```bash
# login using GCloud CLI
gcloud auth application-default login

export GOOGLE_CLOUD_PROJECT=my-project
export MODEL=google-vertex:gemini-2.5-pro-preview-03-25

python main.py
```

### xAI Grok

```bash
export MODEL=openai:grok-3-mini-beta
export OPENAI_API_KEY=your-grok-api-key
export OPENAI_BASE_URL=https://api.x.ai/v1

python main.py
```

### DeepSeek

```bash
export MODEL=openai:deepseek-chat
export OPENAI_API_KEY=your-deepseek-api-key
export OPENAI_BASE_URL=https://api.deepseek.com/v1

python main.py
```

### OpenRouter

```bash
export MODEL=openrouter:meta-llama/llama-4-maverick
export OPENAI_API_KEY=your-openrouter-api-key
export OPENAI_BASE_URL=https://openrouter.ai/api/v1

python main.py
```

## Running Hugo

```bash
hugo server
``````

Access the website locally at http://localhost:1313.

<!-- links -->
[hugo]: https://gohugo.io
[pydantic-ai]: https://ai.pydantic.dev
[pydantic-models]: https://ai.pydantic.dev/models/
