# Spotify Popcount Cascading Failure (2013)

**Company:** Spotify
**Year:** 2013
**Severity:** P1
**Category:** Cascading service failure

## Timeline
On April 27, 2013, Spotify experienced a major outage affecting music playback and login functionality for many European users. The incident began when Spotify’s Popcount service, responsible for storing playlist subscriber counts, became overwhelmed by excessive request traffic. A newly rolled-out Discovery feature had unintentionally introduced additional load by depending directly on Popcount for playlist data. As latency increased, legacy desktop clients repeatedly retried failed requests without exponential backoff, causing request queues to explode. Excessive logging on Accesspoint servers further degraded performance, eventually making many Accesspoints unreachable or extremely slow. Engineers ultimately firewall-blocked the overloaded Accesspoints and hard-reset some servers to stabilize the system. Once clients backed off and traffic normalized, services recovered.

## Root Cause
The outage was caused by a combination of architectural and client-side failures. A newly introduced dependency between the Discovery service and Popcount dramatically increased request volume against an underprovisioned backend service. At the same time, legacy desktop clients contained faulty retry logic that aggressively retried timed-out requests without any backoff mechanism. Excessive error logging on Accesspoint servers amplified the failure by overwhelming disk I/O and making servers increasingly unresponsive, creating a cascading feedback loop throughout the platform.

## Resolution
Spotify engineers first attempted to reduce load by removing the Discovery service dependency on Popcount through a hotfix. When this proved insufficient, teams firewall-blocked overloaded Accesspoint servers to force client disconnects and trigger proper exponential backoff behavior in Spotify clients. Some servers required hard resets before firewall rules could be applied. Once traffic pressure subsided and queues drained, the service gradually returned to normal operation.

## Learnings
Spotify concluded that the original retry bug identified during an earlier Popcount incident should have been treated with much higher urgency. The company implemented fixes for faulty retry behavior in desktop clients, added caching and TTL protections for Discovery data, improved logging rate limits, separated critical logs from noisy logs, and introduced syslog improvements to reduce disk I/O pressure. The incident also reinforced the importance of resilience testing under extreme latency and degraded network conditions.