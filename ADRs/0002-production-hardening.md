# ADR-0002: Production hardening
FinOps HTTP contracts use FastAPI and OpenTelemetry. Kubernetes/Helm package bounded services; Terraform owns infrastructure inputs. Trivy/CycloneDX gate security/SBOM; contract/property tests protect usage APIs; Locust validates load.
Cost attribution and budgets remain domain-owned; production externalizes durable usage state, secrets and telemetry.
