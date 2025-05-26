+++
date = '2025-04-18T09:52:18.035067+00:00'
title = 'Embedding policy as code in GitOps workflows'
summary = 'Learn how to integrate Open Policy Agent and Conftest into your GitOps pipeline, write a Rego rule to block mutable image tags, and configure OPA audit logging for real-time compliance reporting.'
draft = 'false'
model = 'openai:o4-mini'
tags = ["gitops", "policy as code", "compliance"]
+++

Regulated environments demand proof of compliance with every change. You push infrastructure updates multiple times a day. Manual audits lag behind.

In this post, you will learn how to integrate the Open Policy Agent (OPA) and Conftest into your GitOps pipeline, write Rego rules to block mutable image tags, and configure OPA audit logs to report policy violations automatically.

## Challenges in traditional compliance auditing

Audits often run weeks after deployment. You scramble to fix issues under time pressure. By then you may have lost the context of why a configuration changed. This delays releases and raises risk.

## What is policy as code

Policy as code means you author compliance rules in a human-readable language and store them alongside your infrastructure code. Every change triggers a policy check in your version control system.

Open Policy Agent (OPA) is an engine for evaluating policies written in Rego. See the OPA docs: https://www.openpolicyagent.org/docs/latest/. Conftest is a command-line tool that uses OPA to test configuration files before you apply them. See the Conftest docs: https://www.conftest.dev/.

## Integrating policy as code in GitOps workflows

GitOps uses Git as the source of truth for your declarative infrastructure. You merge a pull request to deploy changes. You can plug policy checks into this same workflow.

1. Create a policy repository. Store your Rego rules under a `policy/` directory.
2. Add a CI job. In GitHub Actions or GitLab CI, invoke Conftest or OPA before merging changes. Reject pull requests when policies fail.
3. Deploy policies to your cluster. Use OPA Gatekeeper or the OPA admission controller to enforce rules at runtime.

Below is a CI snippet that runs Conftest against your Kubernetes manifests before merging.

```bash
# run policy tests on Kubernetes manifests to reject unsafe changes early
echo "Checking policies..."
conftest test ./manifests --policy policy/
```

This command ensures every manifest change passes your policies. It rejects pull requests with violations.

## Example: disallow latest image tag

Using the `latest` tag in production leads to unpredictable deployments. A rule to block it ensures you use immutable tags and reproduce past environments.

```rego
package kubernetes.admission

# deny pods that use image:latest
deny[msg] {
  input.request.kind.kind == "Pod"
  container := input.request.object.spec.containers[_]
  endswith(container.image, ":latest")
  msg := sprintf("container %v uses latest tag", [container.name])
}
```

This Rego rule inspects admission requests for pods. It denies any pod whose container image ends with `:latest`. The `msg` explains which container violated the rule.

To test a pod manifest before you merge, run:

```bash
# validate pod.yaml against your policies
conftest test pod.yaml --policy policy/
```

If the manifest declares a `latest` tag, Conftest will return an error and prevent the merge.

## Monitoring and reporting

OPA can emit audit logs in JSON. You forward these logs to a centralized store for reporting and search.

```yaml
# opa-config.yaml
services:
  - name: policy           # OPA service name for policy decisions
    url: https://localhost:8181/v1  # endpoint for policy queries
labels:
  audit: true              # mark all decisions for audit logging
```

The `services.url` field tells OPA where to fetch or evaluate policies. The `labels.audit: true` flag instructs OPA to include every decision in the audit log. You can query logs for `deny` events to trace policy breaches.

Forward these logs to Elasticsearch or Splunk. You gain a searchable history of violations. You answer audit questions with precise data.

## Next steps

Start by writing your highest-value rules in Rego. Store them in a GitOps repo. Plug Conftest or OPA into your CI pipeline. Deploy OPA Gatekeeper in your Kubernetes clusters.

With policy as code, you build compliance into every pull request. You get real-time feedback. You ship faster with confidence.