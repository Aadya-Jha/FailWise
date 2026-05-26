# AWS S3 US-EAST-1 Outage (2017)

**Company:** AWS
**Year:** 2017
**Severity:** P0
**Category:** Operational failure

## Timeline
On February 28, 2017 at 9:37 AM PST, an AWS engineer executed a command intended to remove a small number of servers from an S3 billing subsystem in the US-EAST-1 region. Due to an incorrect input, a much larger set of servers was removed, impacting critical S3 subsystems responsible for metadata management and storage allocation. As these systems restarted, Amazon S3 became unable to process GET, LIST, PUT, and DELETE requests. Multiple AWS services depending on S3, including EC2, EBS, Lambda, and the AWS Service Health Dashboard, were also affected. Partial recovery began at 12:26 PM PST, and full S3 recovery completed by 1:54 PM PST.

## Root Cause
The outage was caused by an operational mistake during maintenance on the S3 billing subsystem. An incorrect command input removed more server capacity than intended, affecting the S3 index and placement subsystems. These systems were critical for object metadata management and storage allocation. Because these large subsystems had not been fully restarted in many years, recovery and integrity validation took significantly longer than expected.

## Resolution
AWS engineers restarted the affected S3 subsystems and gradually restored service functionality. The index subsystem recovered first, allowing GET, LIST, and DELETE operations to resume. The placement subsystem recovered later, restoring PUT operations. Additional AWS services that depended on S3 also recovered after clearing accumulated backlogs. AWS also modified operational tooling to slow capacity removal and added safeguards preventing subsystems from dropping below minimum safe capacity levels.

## Learnings
AWS implemented several changes following the incident. The company added stronger safety checks to operational tools, improved safeguards around capacity removal, and accelerated efforts to partition S3 systems into smaller cells to reduce recovery times and blast radius. AWS also redesigned the Service Health Dashboard administration system to operate across multiple regions so status communication would remain available during future regional outages.