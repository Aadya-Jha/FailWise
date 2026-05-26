# Atlassian Cloud Site Deletion Incident (2022)

**Company:** Atlassian
**Year:** 2022
**Severity:** P0
**Category:** Operational failure

## Timeline
On April 5, 2022 at 07:38 UTC, an internal maintenance script unintentionally deleted 883 Atlassian cloud sites affecting 775 customers. Impacted customers lost access to products including Jira, Confluence, Opsgenie, Statuspage, and Atlassian Access. The first customer support ticket was created at 07:46 UTC, and Atlassian formally triggered a major incident response at 08:17 UTC. Engineers identified the root cause by 08:53 UTC and began large-scale restoration efforts. The recovery process required rebuilding customer sites and restoring distributed product data across multiple services and databases. Some customer sites were restored beginning April 8, while complete restoration of all affected customers finished on April 18, 2022.

## Root Cause
The outage was caused by an operational mistake during removal of a legacy “Insight – Asset Management” application. A communication gap between teams caused cloud site IDs to be provided instead of application IDs to a deletion script. The deletion API accepted both site and app identifiers without validation or warning mechanisms. As a result, the script deleted entire customer sites rather than only the intended application instances. Existing peer-review and staging processes failed to detect the issue because the incorrect production IDs did not exist in staging environments.

## Resolution
Atlassian assembled a large-scale cross-functional incident response team and implemented multiple restoration strategies. Initial recovery efforts focused on manually rebuilding deleted sites and restoring customer data from backups. Engineers later developed a faster “Restoration 2” process that reused original site identifiers and parallelized restoration steps across services. Atlassian also imposed a company-wide code freeze to reduce additional operational risk during recovery. Throughout the incident, teams rebuilt customer contact information, restored support workflows, and coordinated validation with affected customers.

## Learnings
Atlassian implemented immediate safeguards to block bulk site deletions and began introducing universal soft-delete protections across systems. The company accelerated development of automated disaster recovery tooling for large-scale multi-site restoration events and committed to more extensive disaster recovery testing. Atlassian also improved incident management procedures for large-scale outages and strengthened customer communication processes, including backup storage of customer contact information and enhanced support tooling for deleted-site scenarios.