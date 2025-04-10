+++
date = '2025-04-15T08:06:06.969164+00:00'
title = 'Shifting left on infrastructure: security, compliance, and observability in Terraform workflows'
summary = 'How to move security, compliance, and observability to the start of your Terraform workflow by using policy as code, automated checks, and standardized modules, with practical examples and actionable advice.'
draft = 'false'
model = 'openai:gpt-4.1'
tags = ["terraform", "infrastructure as code", "security", "compliance", "observability"]
+++

## Why shifting left matters in Terraform workflows

Pushing security, compliance, and observability tools into the earliest stages of your Terraform workflow isn’t just a best practice. It’s essential if you want your infrastructure to be robust and auditable from day one. Waiting until deployment to think about these requirements leads to painful surprises, expensive rework, and higher risk. By shifting left, you force issues to the surface early, making remediations faster and less disruptive.

You’re probably already using infrastructure as code (IaC) to define resources. So, how do you also make security, compliance, and observability first-class concerns in that workflow?

## Security: build protection into every plan

With Terraform, you describe infrastructure before running it. That planning phase is the right moment to inject security checks.

*Policy as code* is a proven approach. Tools like [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) and [HashiCorp Sentinel](https://www.hashicorp.com/sentinel) let you write policies in code, then enforce them against your Terraform plans. For example, you can mandate that S3 buckets aren’t publicly exposed, or that encryption is always enabled.

```hcl
# Example: Policy requiring S3 encryption
resource "aws_s3_bucket" "example" {
  bucket = "my-secure-bucket"
  # ...
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
```

Using tools like [tfsec](https://aquasecurity.github.io/tfsec/) or [Checkov](https://www.checkov.io/), you can scan code for risky patterns before you ever reach the cloud. Integrate these checks in pull requests. They’ll block merges unless issues are fixed, closing the feedback loop early.

## Compliance: automate enforcement, not documentation

Compliance failures create audit headaches and sometimes legal risk. Instead of auditing by hand after the fact, embed compliance requirements as code.

Define reusable and reviewed Terraform modules for compliant resources. For example, create a standardized module for an internal load balancer that enforces specific network ACLs and tagging policies. Require all teams to use it.

Pair this with automated checks. Tools like [Terraform Cloud’s policy sets](https://developer.hashicorp.com/terraform/cloud-docs/policy/overview) can globally enforce controls, such as making sure resources have mandatory tags (for accounting or tracking). You edit code to fix compliance gaps—never spreadsheets.

## Observability: visibility from the start

If you want to know what’s happening in your infrastructure, you need to configure monitoring and logging at the time you create resources, not after.

Write modules that always create the required log groups, metrics, and alerts. For example, an AWS EC2 module can embed CloudWatch logs and alarms definitions, ensuring that when an instance comes up, monitoring is already active.

Tie observability standards to your security and compliance modules. Don’t just require a database encryption policy—require that access logs are shipped to a central location. This helps during incident response and forensic analysis.

## Integrating it all: examples and workflows

Here’s a practical flow:

1. Developers open a pull request with Terraform changes.
2. Automated checks (tfsec, Checkov, OPA policies) run in CI/CD pipelines.
3. Policy compliance and required modules are verified. If a change violates a security policy or skips observability, it fails.
4. Only passing changes are merged.
5. Audit trails and logs are enforced by code, not docs.

This feedback loop is fast. Developers see violations immediately, not days later. Problems get fixed before deployments, slashing costs and risk.

## Key takeaways

- Make policies and standards part of the code, not an afterthought.
- Use policy as code tools and automated scanners early and everywhere.
- Standardize secure, compliant, observable modules, and require their use.
- Surface all issues in code review, not post-deployment.

You will spend less time firefighting and more time building useful infrastructure. That’s the real benefit of shifting left in Terraform workflows.

## References
- [Open Policy Agent](https://www.openpolicyagent.org/)
- [tfsec](https://aquasecurity.github.io/tfsec/)
- [Checkov](https://www.checkov.io/)
- [Terraform Cloud Policy](https://developer.hashicorp.com/terraform/cloud-docs/policy/overview)
