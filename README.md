# AI generated blog

[![Netlify Status](https://api.netlify.com/api/v1/badges/1a34df76-38de-42a1-8bcc-074f144a4b83/deploy-status)](https://app.netlify.com/sites/ai-generated-tech-blog/deploys)

This repository demonstrate the use of [Pydantic AI](https://ai.pydantic.dev)
together with [Hugo](https://gohugo.io/) to generate blog posts on a given
topic using various models (OpenAI ChatGPT 4o, Gemini).

> [!WARNING]
>  This project is not intended to flood the web with low-quality AI-generated
>  content. The goal is to explore and demonstrate how different AI models can
>  assist in generating blog posts. Use this responsibly and with a focus on
>  transparency, originality, and value.

```mermaid
flowchart TD
    A[Topic Agent]
    B[Post Agent]
    C[Feedback Agent]
    D{Quality score > 0.8 ?}

    E(Publish post)

    A -- Generate topic that doesn't<br>overlap with existing posts --> B
    B -- Draft post --> C
    C --> D
    D -- Yes --> E
    D -- No, provide feedback and<br>ask to revisit --> B
```

## Generating blog posts

```bash
cd ai/
# if using OpenAI, refer to the pydantic ai documentation for other models
export OPENAI_API_KEY=your-api-key
export MODEL=openai:gpt-4.1
python main.py
```

## Running Hugo

```bash
hugo server
``````

Access the website locally at http://localhost:1313.
