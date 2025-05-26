+++
date = '2025-04-16T07:04:44.980609+00:00'
title = 'Platform engineering anti-patterns: lessons from teams who tried to build it all'
summary = 'Many teams fail at platform engineering by trying to build everything in-house. Learn concrete anti-patterns, with examples, and practical lessons on focus, sustainability, and user-driven internal platform development.'
draft = 'false'
model = 'openai:gpt-4.1'
tags = ["platform engineering", "devops", "internal developer platform"]
+++

Building internal platforms can transform how your organization creates and operates software. But many teams stumble by trying to do everything themselves. That approach is more common than you might think—and it brings hard lessons. This post looks at real problems teams have faced when attempting to “build it all,” along with concrete takeaways you can use to avoid their mistakes.

## Why teams choose to build everything

Platform engineering aims to simplify and standardize how developers run, deploy, and operate applications. Teams get excited about building a platform tailored to their organization’s tools and workflows. Sometimes, they want control over every aspect and think custom builds deliver a competitive edge. Sometimes, existing solutions look expensive or inflexible. So, teams commit to designing and developing workflows, frameworks, infrastructure, and tooling entirely in-house.

## The anti-patterns: where build-it-all goes wrong

### Reinventing the wheel instead of using proven tools

One anti-pattern is replicating commercial or open-source software instead of adopting it. For example, teams often attempt to create homegrown continuous integration/continuous deployment (CI/CD) pipelines, internal container orchestrators, or bespoke monitoring stacks. 

This usually leads to functionality gaps or reliability issues. A homegrown CI/CD tool may miss crucial integrations or lack security features present in mature options like Jenkins, GitHub Actions, or GitLab.

### Underestimating maintenance and support load

Internal platforms need as much care as public-facing products. Some teams think once they launch internal tools, the burden ends. But updates, bug fixes, and requests pile up fast. As a result, internal users get frustrated. Technical debt grows. 

Netflix shared that their Internal Developer Platform (IDP) required more ongoing investment than anticipated. Maintaining even well-designed internal platforms stretched engineering capacity (
https://thenewstack.io/building-platforms-at-netflix-a-look-under-the-hood/
).

### Ignoring developer experience and feedback

Teams sometimes over-optimize for infrastructure requirements and forget about day-to-day developer needs. Users find homegrown platforms confusing or unreliable. Without regular feedback and quick iteration, the platform becomes a blocker instead of an enabler.

Spotify found success by investing intentionally in Internal Developer Portals with clear documentation and a feedback loop (
https://backstage.spotify.com/blog/platform-thinking/
). Teams who ignored developer input drifted into obscurity.

### Lack of focus: trying to solve all problems at once

Trying to satisfy every team’s workflow or tooling request results in platforms that are overly complex and hard to use. The result: nobody’s workflow fits well. 

Instead, teams should focus on shared pain points and high-impact features. This keeps scope manageable and delivers real value.

### Burnout and turnover from always being on-call

Running critical internal infrastructure is a 24/7 responsibility. Teams that do not plan for on-call work, knowledge sharing, and backup rotation end up with thin coverage and people exhausted by constant firefighting.

## Lessons learned: what successful teams do differently

- *Start with buy, not build.* Only build what gives you unique advantage or cannot be found off the shelf.
- *Solve for real, shared problems first.* Interview users and analyze support tickets. Prioritize common pain points.
- *Automate sustainability.* Plan for versioning, upgrades, quality checks, and clear deprecation policies from the start.
- *Keep a product mindset.* Treat your internal platform as a service with real users and outcomes.
- *Close the feedback loop.* Gather feedback early and often—even before launch. Iterate based on how people really use the platform.

## Final thought

It’s tempting to “own it all” when building a platform. But the most effective teams know when to leverage existing solutions, focus their efforts, and treat their internal tools as products. Learn from those who tried to do everything—and run into trouble—so your engineering platform serves your users, not the other way around.
