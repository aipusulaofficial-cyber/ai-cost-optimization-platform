# Principal Engineering

## Scope

This platform provides AI cost optimization APIs and telemetry-oriented cost controls. The engineering boundary covers the service contract, deterministic cost-domain behavior, operational health endpoints, CI quality gates, supply-chain evidence, and hardened deployment manifests.

## Enforced controls

- [x] CI uses least-privilege workflow permissions.
- [x] Third-party GitHub Actions are pinned to immutable commit SHAs.
- [x] Checkout does not persist repository credentials.
- [x] CI and security jobs have explicit timeouts.
- [x] Automated tests and coverage are enforced in CI.
- [x] Dependency/security scanning and CycloneDX SBOM generation run in Actions.
- [x] Kubernetes, Helm, and Terraform deployments use a non-root UID/GID 10001.
- [x] Kubernetes workloads use RuntimeDefault seccomp, no privilege escalation, read-only root filesystems, and all Linux capabilities dropped.
- [x] Deployment manifests define resource requests/limits and readiness/liveness probes.
- [x] Deployment images use the release version 0.1.0 rather than the mutable latest tag.
- [x] Helm autoscaling and disruption configuration remain explicit.

## Evidence boundary

A repository is considered GREEN when the configured CI, production-test, and supply-chain gates pass on the current main commit. This is repository-level engineering evidence; it is not a claim of environment-independent production certification.
