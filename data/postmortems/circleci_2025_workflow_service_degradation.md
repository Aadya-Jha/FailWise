# CircleCI Workflow Service Degradation (2025)

**Company:** CircleCI
**Year:** 2025
**Severity:** P1
**Category:** Database migration failure

## Timeline
On April 4, 2025, between 22:08 UTC and 23:45 UTC, CircleCI customers experienced delays and failures when starting or canceling workflows and jobs. The incident began during a planned upgrade to the workflows service database using a blue/green deployment strategy. Shortly after deployment, engineers observed increased latency and job failures caused by exhausted retry queues. Additional engineers joined the incident response, database resources were increased, and non-critical operations were disabled to stabilize the system. When performance did not improve sufficiently, the team rolled back to the old database at 23:19 UTC. Services fully recovered by 23:45 UTC.

## Root Cause
The outage was caused by stale database statistics after a major version upgrade during the blue/green deployment process. An analyze operation intended to rebuild database statistics was executed too early and became outdated after a second major version upgrade within the same deployment. As a result, database queries failed to use indexes efficiently and instead hit disk heavily, causing severe latency and workflow queue buildup.

## Resolution
Engineers attempted multiple mitigations including restarting workflow service pods, scaling database resources, disabling non-critical database operations, and reducing service load by scaling down workflows pods. When these efforts did not restore acceptable performance, the team reverted traffic back to the previous database version and reinstated it as the primary database. Workflow queues gradually recovered and normal operations resumed.

## Learnings
CircleCI updated its blue/green deployment procedures to ensure database analysis operations are performed after every major version change. The team also introduced additional automated tests and manual checkpoints before future migrations to identify issues earlier. Further testing was conducted to validate that running analyze operations during heavy database load would not worsen performance.