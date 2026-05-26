# Netflix Response to AWS EBS Degradation (2012)

**Company:** Netflix
**Year:** 2012
**Severity:** P2
**Category:** Availability zone failure

## Timeline
On October 22, 2012, AWS experienced degradation in its EBS service that affected many major websites. Netflix first noticed issues affecting external websites shortly after 8:30 AM but initially observed no internal service impact. Around 11:00 AM, some Netflix customers began experiencing intermittent issues, and by 11:15 AM Netflix opened an internal incident investigation. Engineers identified the issue as a network-related problem isolated to a single AWS Availability Zone. Once AWS confirmed the degradation was limited to one zone, Netflix initiated a full evacuation of the affected zone. The evacuation completed in approximately 20 minutes, restoring normal service for customers.

## Root Cause
The degradation originated from an AWS Availability Zone experiencing EBS and networking issues. Although Netflix avoided relying heavily on EBS for persistence, network degradation within the affected zone still caused intermittent customer-facing issues. The incident itself was external to Netflix infrastructure, but Netflix’s systems experienced partial impact from dependency failures inside the degraded AWS zone.

## Resolution
Netflix engineers leveraged existing zone evacuation tooling and operational procedures developed from prior resilience exercises. Traffic was redirected away from the affected Availability Zone and applications were reconfigured to operate entirely from the remaining healthy zones. Cassandra clusters automatically routed around unavailable replicas and repaired themselves after recovery. The zone evacuation process completed quickly due to extensive automation and prior disaster recovery drills.

## Learnings
The incident reinforced Netflix’s investment in multi-Availability Zone redundancy, automated failover tooling, and resilience testing through the Simian Army suite, including Chaos Monkey and Chaos Gorilla. Netflix also identified opportunities to improve incident detection speed and simplify zone evacuation further through additional automation. The company continued developing resilience strategies for even larger-scale outages, including full regional failure testing.