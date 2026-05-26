# Heroku API and Dashboard Outage (2023)

**Company:** Heroku
**Year:** 2023
**Severity:** P1
**Category:** Database failure

## Timeline
On June 8, 2023 at 15:05 UTC, Heroku experienced a database-related failure that prevented customers from creating new authorizations and deployments. For approximately 1 hour and 45 minutes, customers were unable to log in or deploy new releases. Starting at 16:50 UTC, the issue escalated into a broader API outage affecting the Heroku Dashboard, CLI, webhooks, and other application management functions. Running applications continued operating normally throughout the incident. Engineers restored normal API operations by 18:57 UTC.

## Root Cause
The incident was caused by a database schema mismatch where a foreign key column used a smaller data type than the primary key it referenced. When the primary key value exceeded the foreign key’s allowable range, an overflow error occurred, preventing creation of new authorizations and deployments. During remediation, a database migration corrected the data type mismatch but unintentionally cleared internal PostgreSQL statistics, significantly degrading query performance and triggering a wider API outage.

## Resolution
Engineers performed a database migration to update the foreign key type and restore authorization functionality. After query performance degraded, the Heroku API was temporarily switched into read-only mode while engineers repaired the database statistics issue. Once database performance stabilized, the API returned to normal read/write operation and the incident was officially resolved.

## Learnings
Heroku planned several improvements following the incident. The company introduced better tooling to monitor database schema consistency and detect foreign keys approaching data type limits. They also updated migration playbooks to ensure database statistics are properly refreshed after schema changes, reducing the risk of performance degradation during future migrations.