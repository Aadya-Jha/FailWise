# Discord Cascading Service Failure (2017)

**Company:** Discord
**Year:** 2017
**Severity:** P1
**Category:** Cascading infrastructure failure

## Timeline
On October 13, 2017 at approximately 14:01, Discord engineers detected anomalies caused by a Redis primary node failure during an automatic Google Cloud Platform migration. The Redis failover exposed known issues in how Discord’s API services handled Redis cluster failovers, causing API instability and latency. Engineers attempted rolling restarts and mitigated several related issues, including a cache misconfiguration and Cassandra cluster overload. Later, additional failures appeared in Discord’s “guilds” and “sessions” clusters, causing servers to appear offline for users. By 16:07, engineers determined that a full system restart was necessary. Discord services gradually recovered beginning at 16:33 and full restoration completed by 16:52.

## Root Cause
The incident began when a Redis primary node was automatically migrated by Google Cloud Platform and unexpectedly dropped offline. Although the Redis cluster failed over correctly, some Discord API instances did not properly handle the failover process due to a previously known bug. The resulting API instability exposed an edge cache misconfiguration that generated excessive requests to an expensive API route, overloading a Cassandra cluster. Additional cascading failures occurred across other distributed system components, eventually causing nodes to enter invalid states and fail due to memory exhaustion.

## Resolution
Discord engineers restarted API services, corrected the edge caching misconfiguration, recovered the overloaded Cassandra cluster, and forcefully restarted failing nodes in the “guilds” and “sessions” clusters. When instability continued spreading across the system, engineers initiated a full platform reboot to reset invalid service states and reconnect clients cleanly. Additional fixes were applied during recovery, including correcting an improperly configured API reconnect setting.

## Learnings
Discord increased the priority of fixing known Redis failover handling bugs and improved caching behavior for problematic API routes. Engineers also added new monitoring and alerting systems to detect cascading failure patterns earlier. Following the incident, the team investigated flaws in an underlying library used by affected services and began deploying updates intended to improve reliability and reduce the risk of future cascading infrastructure failures.