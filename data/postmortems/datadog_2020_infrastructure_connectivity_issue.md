# Datadog US Region Service Degradation (2020)

**Company:** Datadog
**Year:** 2020
**Severity:** P1
**Category:** Infrastructure failure

## Timeline
Between September 24, 2020 14:27 UTC and September 25, 2020 00:40 UTC, Datadog’s US region experienced widespread service degradation. Multiple core services including the web tier, logs, alerts, infrastructure monitoring, APM, and network monitoring were intermittently unavailable or degraded. The web tier suffered particularly high error rates, with dashboards sometimes refreshing successfully only 10–40% of the time. Services gradually recovered over several hours as engineering teams stabilized the underlying infrastructure.

## Root Cause
The outage was caused by the failure of Datadog’s internal service discovery and dynamic configuration system. A faulty configuration change introduced a dependency on the local DNS resolver instead of static local files. During a routine recycle of a latency-measuring cluster, the system generated a massive spike in DNS requests. This created a “thundering herd” effect that overloaded the service discovery cluster, causing it to lose quorum and fail. As a result, many services could no longer reliably discover dependencies or retrieve runtime configurations.

## Resolution
Engineering teams created an internal war room and worked to stabilize the service discovery cluster by isolating it from excessive traffic and carefully reintroducing clients. Teams also temporarily removed dependencies on the failed service discovery system by relying on static configurations where possible. Services were progressively restored as the cluster stabilized and downstream systems recovered.

## Learnings
Datadog identified several improvements to prevent similar incidents in the future. The company began separating service discovery and dynamic configuration into independent systems, adding additional caching layers, and improving resilience against prolonged service discovery failures. They also planned to reduce hard dependencies in the web tier, improve incident communication processes, and create clearer recovery playbooks for regional failures.