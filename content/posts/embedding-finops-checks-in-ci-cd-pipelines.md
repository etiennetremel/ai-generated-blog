+++
date = '2025-04-17T16:31:37.734461+00:00'
title = 'Embedding FinOps checks in CI/CD pipelines'
summary = 'Turn cloud costs into actionable tests by adding money checks to CI/CD. Learn why cost belongs next to unit tests, which tools to use, and how to fail builds when budgets break.'
draft = 'false'
model = 'openai:o3'
tags = ["finops", "ci/cd", "cloud cost"]
+++

You push code, the pipeline runs, tests pass, and the pull request turns green. Minutes later your change lands in
production and doubles the bill. Sound familiar? Cloud cost often hides until after deployment, when it’s too late to
fix cheaply. Let’s tackle that by treating money as another quality gate in your continuous integration and
continuous delivery (CI/CD) pipeline.

## Why cost belongs next to unit tests

Unit tests catch functional bugs before they escape. Security scans catch vulnerabilities. You already break the build
for those. Cost drift is just as real. A mis‑sized instance or an unbounded autoscaling rule can burn thousands of
dollars in hours. Put guardrails where developers work: inside the pipeline, not in monthly reports.

Benefits are concrete:

* Fast feedback: developers learn the impact of a change in minutes, not after the invoice.
* Lower rework: fixing cost while code is fresh is cheaper than rolling back in production.
* Shared ownership: finance, ops, and engineering see the same result in the same place.

## What makes a good cost check

A cost test should be:

1. Deterministic: given the same code and inputs, it returns the same number.
2. Actionable: failures link to the exact lines or resources causing the overrun.
3. Policy‑driven: thresholds come from a version‑controlled file, not tribal knowledge.
4. Fast: add seconds, not minutes, to the pipeline.

## Picking the right tools

Several open‑source and commercial projects already expose cost data in a test‑friendly format.

| Tool | Works with | Output format | Notes |
| --- | --- | --- | --- |
| Infracost | Terraform, Terragrunt, Pulumi (preview) | JSON, GitHub comments | Uses public or private price books |
| Cloud Custodian | AWS, Azure, Google Cloud | YAML audit | Policy engine that can run in CI or on a schedule |
| Open Policy Agent (OPA) with Cloud Pricing API | Any JSON plan | Rego rules | High flexibility, steeper learning curve |

You don’t need to adopt new infra-as-code to start. Most tools can read the generated cloud formation or plan file as
input.

## Example: fail the build when Terraform cost grows more than 5 %

Below is a trimmed GitHub Actions workflow. It assumes Terraform code lives in `infra/` and you installed the
`infracost` CLI.

```yaml
name: ci-cost-check
on: [pull_request]

jobs:
  cost:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: set up terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.4

      - name: terraform plan
        working-directory: infra
        run: |
          terraform init -input=false
          terraform plan -out=tfplan.binary -input=false
          terraform show -json tfplan.binary > tfplan.json

      - name: infracost breakdown
        run: |
          infracost breakdown --path=tfplan.json \
            --format=json --out-file=infracost-base.json

      - name: infracost diff
        id: cost
        run: |
          infracost diff --path=tfplan.json \
            --format=json --compare-to=infracost-base.json \
            --out-file=infracost-diff.json

      - name: evaluate cost diff
        run: |
          delta=$(jq '.diffTotalMonthlyCostPercent' infracost-diff.json)
          echo "Cost delta ${delta}%"
          if (( $(echo "$delta > 5" | bc -l) )); then
            echo "Cost increase above threshold. Failing build."
            exit 1
          fi
```

Why this works:

* `terraform show -json` produces a machine‑readable plan.
* Infracost converts resource changes into price estimates.
* We compare against the `main` branch baseline stored in the artifact.
* A simple Bash gate enforces the 5 % rule and terminates the job if violated.

Developers now see a red ✗ next to their pull request along with a comment listing the most expensive resources.

## Dealing with non‑deterministic prices

Spot instances, pay‑per‑request services, and demand‑based autoscaling complicate unit‑style testing. Handle them with
input variables and scenarios. For example, set a conservative upper bound on request volume or instance hours, then
codify that assumption in the `cost_policy.yml` checked into git. Document these choices so reviewers understand the
context.

## Policy as code: sample Rego rule

If you already use Open Policy Agent, add cost to your existing security rules. The snippet below denies any Kubernetes
namespace that would exceed USD 200 per month based on a side‑loaded price list.

```rego
package finops

max_namespace_cost = 200

deny[msg] {
  input.kind == "Deployment"
  cost := input.metadata.annotations["estimated_monthly_cost"]
  cost > max_namespace_cost
  msg := sprintf("Deployment %s exceeds budget: $%.2f", [input.metadata.name, cost])
}
```

Feed the rule with a JSON doc generated by your favorite estimator. The CI job fails when `deny` emits any message.

## Integrating with pull request reviews

Cost data must be visible where developers already look. Most tools can post rich comments like:

```
💰  Monthly cost will increase by $78 (+12%)
  • aws_instance.app_server +$50
  • aws_rds.mysql       +$28
```

Pair this with line‑level annotations (`git diff` hints) for an almost unit‑test‑like experience.

## Getting the threshold right

Start simple: block changes that raise total monthly cost by more than a single‑digit percentage. Then refine:

* Per‑environment budgets (dev, staging, prod).
* Absolute caps on risky resources, e.g., `r5.24xlarge`.
* Tag‑based rules: only the data team can approve Redshift clusters.

Store numbers in version control. When finance adjusts budgets, submit a pull request, not an email.

## Common pitfalls

| Pitfall | How to avoid |
| --- | --- |
| Treating cost as advisory only | Make the pipeline fail. Green buttons change behaviour. |
| Missing shared resources | Model baseline correctly or you’ll blame the wrong change set. |
| Ignoring usage‑based services | Use representative traffic figures and refresh them quarterly. |
| Slow estimations | Cache price data and scope the plan to changed modules. |

## Beyond build: measuring impact in production

Pipeline tests catch regressions early but can’t predict everything. Complement them with runtime metrics:

* Cost per request (link budgets to performance dashboards). 
* Budgets in the cloud provider API with auto‑shutdown alarms. 
* Daily anomaly detection jobs.

Feedback the real spend into your policy thresholds to keep them honest.

## Takeaway

You already block a merge when a unit test fails. Do the same when cost explodes. Adding a 20‑line step to your
pipeline turns abstract FinOps goals into a concrete, testable contract developers cannot ignore. Start with one
team, one threshold, and iterate.
