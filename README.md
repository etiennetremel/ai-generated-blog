# AI generated blog

[![Netlify Status](https://api.netlify.com/api/v1/badges/1a34df76-38de-42a1-8bcc-074f144a4b83/deploy-status)](https://app.netlify.com/sites/ai-generated-tech-blog/deploys)

This repository demonstrate how to use [Pydantic AI][pydantic-ai] with
[Hugo][hugo] to generate blog posts on a given topic using different models
(OpenAI ChatGPT 4o, Gemini).

> [!WARNING]
>  This project is not intended to flood the web with low-quality AI-generated
>  content. The goal is to explore and demonstrate how different AI models can
>  assist in generating blog posts. Use this responsibly and with a focus on
>  transparency, originality, and value.

## Overview

The diagram below outlines the end-to-end workflow for generating blog posts.

```mermaid
flowchart TD
    A[Start]
    B((Topic Agent))
    C((Post Agent))
    D((Feedback Agent))
    E{Quality score > 0.8 ?}
    F(Editorial guideline)
    G[Publish post]
    H[End]
    I(Existing blog posts)

    A ==> B
    B -.-> I
    B == Generate topic that doesn't<br>overlap with existing posts ==> C
    C == Draft post ==> D
    C -.-> F
    D -.-> F
    D ==> E
    E == Yes, format post<br>with metadata ==> G
    E -- No, provide feedback and<br>ask to revisit --> C
    G ==> H
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

## Running Hugo

```bash
hugo server
``````

Access the website locally at http://localhost:1313.

<!-- links -->
[hugo]: https://gohugo.io
[pydantic-ai]: https://ai.pydantic.dev
[pydantic-models]: https://ai.pydantic.dev/models/
