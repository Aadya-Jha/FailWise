# GitHub Database Cluster Outage (2012)

**Company:** GitHub
**Year:** 2012
**Severity:** P1
**Category:** Database failover failure

## Timeline
In September 2012, GitHub experienced two major outages that caused approximately 1 hour and 46 minutes of downtime along with additional periods of degraded performance. The incidents began after a database migration generated unusually high load on GitHub’s new MySQL cluster infrastructure. Automated failovers repeatedly moved the active database role between nodes, causing instability and poor performance due to cold database caches. On the following day, attempts to recover cluster state triggered a Pacemaker segmentation fault that caused a cluster partition and database inconsistencies. GitHub shut down an out-of-date database node to prevent further data corruption, temporarily taking down production database access and the GitHub website.

## Root Cause
The outage was caused by failures in GitHub’s automated database failover and cluster management systems. High database load during a schema migration triggered false health check failures, causing unnecessary failovers. Later, disabling maintenance mode triggered a Pacemaker segfault that partitioned the database cluster into conflicting states. An out-of-date node was incorrectly elected as master, creating replication inconsistencies and causing temporary exposure of some private repository metadata.

## Resolution
GitHub engineers disabled problematic automated failover behavior and manually recovered the database cluster. The out-of-date node was powered off to stop further data drift, and Pacemaker and Heartbeat services were restarted to restore a clean cluster state. Engineers restored MySQL services on healthy nodes and gradually recovered site performance as database caches warmed back up. GitHub also audited incorrectly routed repositories and notified affected users.

## Learnings
GitHub concluded that fully automated failover was not appropriate for its primary production database systems. The company updated Pacemaker configurations so failovers would require explicit operator approval. Engineers also investigated methods for warming InnoDB buffer pools to reduce recovery impact after failovers. Additional audits and testing were performed on the Pacemaker and Heartbeat stack to identify and prevent future cluster management failures.