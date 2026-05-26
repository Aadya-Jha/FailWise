# Slack Cascading Cache and Datastore Failure (2022)

**Company:** Slack
**Year:** 2022
**Severity:** P1
**Category:** Cascading datastore failure

## Timeline
On February 22, 2022, Slack experienced a major outage that prevented many users from connecting to the platform or completing client boot operations. The incident began shortly after 6:00 a.m. Pacific Time as users and internal monitoring systems reported failures and elevated latency. Slack engineers observed severe overload on a Vitess datastore keyspace responsible for channel membership data. To stabilize the platform, engineers throttled client boot operations, prioritizing already-connected users over new sessions. Attempts to gradually raise traffic limits initially caused renewed overload, forcing stricter throttling. Recovery accelerated after engineers modified problematic database queries and restored cache effectiveness, eventually allowing service to return to normal.

## Root Cause
The outage was triggered during maintenance upgrades of Slack’s Consul service discovery agents. As Consul agents restarted on memcached nodes, Slack’s Mcrib cache control system aggressively replaced and flushed cache nodes, significantly reducing cache hit rates. A high-volume “scatter query” used during client boot operations then became extremely expensive because missing cache entries forced queries across every shard of a heavily loaded Vitess datastore. The resulting database overload prevented caches from refilling, creating a cascading failure loop between the cache and datastore layers. Client retries further amplified load during the incident.

## Resolution
Slack engineers paused the Consul rollout and introduced aggressive throttling on client boot requests to reduce datastore pressure. Engineers also optimized the problematic Group Direct Message membership query so it only queried missing data rather than scanning every datastore shard. Additional changes allowed reads from replicas and improved cache refill behavior. As cache hit rates recovered and database load stabilized, Slack gradually increased client boot traffic back to normal levels.

## Learnings
Slack identified important risks related to cache churn, service discovery interactions, and expensive scatter queries. The company modified rollout procedures for Consul upgrades, redesigned problematic database queries to use more efficient shard keys, and reviewed other cache-backed queries for similar failure patterns. The incident also reinforced the importance of understanding cascading failures, metastable distributed systems behavior, and how efficient local optimizations can unintentionally create globally unsafe system dynamics.