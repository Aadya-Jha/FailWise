# Cloudflare Global Network Outage (2025)

**Company:** Cloudflare
**Year:** 2025
**Severity:** P0
**Category:** Configuration failure

## Timeline
On November 18, 2025 at 11:20 UTC, Cloudflare began experiencing major failures in its core traffic routing systems, causing widespread HTTP 5xx errors across customer websites and services. Initially, engineers suspected a large-scale DDoS attack because of fluctuating failures and simultaneous issues affecting the status page. The incident was later traced to a faulty Bot Management configuration file that was repeatedly generated and propagated across the network. At 14:24 UTC, Cloudflare stopped propagation of the faulty file and tested a rollback using a known-good version. By 14:30 UTC, the primary impact was resolved and most services recovered. Full restoration of all downstream services completed by 17:06 UTC.

## Root Cause
The outage was caused by a permissions-related database change in a ClickHouse cluster used for generating Bot Management feature files. The change unintentionally caused duplicate metadata rows to appear in query results, which doubled the size of the generated feature file. This oversized file exceeded memory allocation limits inside Cloudflare’s proxy routing software, causing the Bot Management module to panic and crash. As the faulty configuration propagated globally, core proxy systems failed and generated widespread HTTP 5xx errors.

## Resolution
Cloudflare engineers investigated multiple possible causes before identifying the faulty Bot Management configuration file. The team stopped generation and propagation of new feature files and manually restored a previously known-good configuration. They also implemented bypasses for Workers KV and Access services to reduce impact while recovery proceeded. After deploying the corrected configuration globally and restarting affected systems, traffic flow and services gradually returned to normal.

## Learnings
Cloudflare identified several areas for improvement following the incident. The company began hardening validation for internally generated configuration files, improving feature kill switches, and reviewing error-handling behavior across all proxy modules. They also planned to prevent debugging systems and crash reporting from overwhelming infrastructure resources during failures. The incident highlighted weaknesses in assumptions around configuration generation and resilience in critical traffic-routing systems.