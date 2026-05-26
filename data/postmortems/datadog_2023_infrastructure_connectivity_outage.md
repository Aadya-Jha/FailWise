# Datadog Multi-Region Infrastructure Connectivity Outage (2023)

**Company:** Datadog
**Year:** 2023
**Severity:** P0
**Category:** Infrastructure networking failure

## Timeline
On March 8, 2023 at 06:03 UTC, Datadog experienced a major multi-region outage affecting the US1, EU1, US3, US4, and US5 regions across nearly all services. Customers lost access to the Datadog platform, APIs, dashboards, monitors, and parts of the telemetry ingestion pipeline. Initial recovery signs appeared around 09:13 UTC when web access was restored, and major services gradually returned throughout the day. Datadog declared all services operational by March 9, 2023 at 08:58 UTC, while full historical data backfilling and complete resolution finished on March 10, 2023 at 06:25 UTC.

## Root Cause
The outage was triggered by an automatically applied systemd security update on Ubuntu 22.04 nodes. When systemd-networkd restarted after the update, it unintentionally deleted networking routes managed by the Cilium Container Network Interface (CNI) plugin. This caused affected Kubernetes nodes to lose internal networking connectivity and go offline. Because a legacy automatic update channel was enabled across multiple regions, the faulty update applied simultaneously across tens of thousands of nodes in several independent cloud regions, dramatically amplifying the impact.

## Resolution
Datadog engineers disabled the problematic security update channel and worked with cloud providers to recover compute capacity across affected regions. Teams restored Kubernetes control planes first, followed by recovery of hundreds of dependent clusters and services. Recovery efforts prioritized restoring real-time telemetry ingestion and alerting before rebuilding historical data systems. Engineers also modified systemd-networkd behavior to preserve routing tables during restarts and audited infrastructure for similar hidden update mechanisms.

## Learnings
Datadog identified weaknesses in assumptions around regional isolation and indirect shared dependencies. The company expanded chaos-testing strategies to simulate larger-scale infrastructure degradation and began prioritizing degraded-mode functionality for critical live telemetry and alerting systems. Datadog also improved customer communication plans for degraded service states and enhanced infrastructure auditing to eliminate unmanaged automatic update channels across production environments.