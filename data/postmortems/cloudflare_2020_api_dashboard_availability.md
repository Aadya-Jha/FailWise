# Cloudflare API and Dashboard Availability Incident (2020)

**Company:** Cloudflare
**Year:** 2020
**Severity:** P1
**Category:** Distributed systems failure

## Timeline
On November 2, 2020 at 14:43 UTC, a network switch in one of Cloudflare’s control plane data centers entered a partially degraded state. Although the switch did not completely fail, it caused inconsistent network communication between nodes in an etcd cluster. This triggered repeated leader election conflicts that made the etcd cluster temporarily read-only. Shortly afterward, Cloudflare’s database management system incorrectly promoted a new primary database, triggering expensive replica rebuilds. One authentication database cluster became overloaded because it temporarily lacked read replicas, causing major degradation to Cloudflare’s API and dashboard services. API success rates dropped as low as 75%, and dashboard operations became up to 80 times slower than normal. Service fully recovered after the first database replica rebuild completed at 21:20 UTC.

## Root Cause
The incident originated from a partially failed network switch that created inconsistent connectivity between nodes in an etcd cluster. This created a distributed systems failure mode similar to a Byzantine or omission fault, where different cluster members had conflicting views of network state. The resulting etcd instability triggered automatic database failover events. A defect in Cloudflare’s database cluster management system required full replica rebuilds after promotion of a new primary database, temporarily removing critical read replicas from service and overloading the primary authentication database.

## Resolution
Cloudflare engineers reduced load on the affected authentication database by throttling non-critical background operations and manually redirecting some API read traffic to replicas in a secondary data center. Engineers also adjusted failover behavior and continued rebuilding database replicas. Once the first replica finished rebuilding and returned to service, database performance normalized and API/dashboard functionality recovered.

## Learnings
Cloudflare identified several architectural improvements following the incident. The company fixed the database cluster management bug that required full replica rebuilds after failover and revisited aggressive automated failover configurations. Engineers also continued redesign work for session handling and cross-datacenter traffic steering to improve resilience during regional degradation events. The incident highlighted the complexity of distributed systems failure modes where partially degraded components can trigger cascading failures despite extensive redundancy.