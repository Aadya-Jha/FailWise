# Reddit Kubernetes Upgrade Outage (2023)

**Company:** Reddit
**Year:** 2023
**Severity:** P0
**Category:** Kubernetes networking failure

## Timeline
On March 14, 2023 at approximately 19:00 UTC, Reddit engineers initiated a Kubernetes upgrade on one of the company’s most critical production clusters supporting legacy Reddit infrastructure. Within minutes, the cluster lost metrics visibility and major parts of Reddit became unavailable, leading to a 314-minute outage. Engineers observed DNS failures, broken service discovery, stalled pod startups, and severe networking instability. Multiple remediation attempts, including restarting control plane services and removing problematic admission controller webhooks, failed to recover the cluster. After more than two hours of investigation, engineers decided to restore the Kubernetes control plane from backups. Recovery efforts were complicated by outdated restore procedures, certificate mismatches, and cloud capacity exhaustion, but the platform gradually recovered as traffic was slowly reintroduced. Full service restoration completed after carefully scaling traffic back to 100%.

## Root Cause
The outage was triggered by a Kubernetes upgrade from version 1.23 to 1.24. Reddit’s Calico networking configuration relied on route reflector rules targeting Kubernetes nodes labeled with `node-role.kubernetes.io/master`. Kubernetes 1.24 removed the legacy `master` label in favor of `control-plane`, causing Calico route reflectors to fail. As a result, network routes between nodes collapsed across the cluster, breaking internal networking, DNS resolution, and service communication. The issue was difficult to diagnose because the specialized route reflector configuration was undocumented, manually managed, and largely unknown to current engineers.

## Resolution
Reddit engineers first attempted to recover the cluster by restarting networking and control plane components, removing admission controller webhooks, and investigating DNS failures. When forward recovery failed, the team restored the Kubernetes control plane from backups and rebuilt the cluster state. Engineers corrected certificate mismatches introduced during restoration, recovered additional control plane nodes, and carefully scaled traffic back online in stages to avoid overwhelming downstream systems and caches.

## Learnings
Reddit identified several major architectural and operational weaknesses during the incident. The company committed to reducing bespoke Kubernetes configurations, improving infrastructure standardization, codifying undocumented networking configurations, and modernizing backup and restore procedures. Engineers also recognized the risks associated with Kubernetes upgrades and legacy infrastructure assumptions, particularly hidden dependencies on deprecated Kubernetes labels and manually managed networking systems.