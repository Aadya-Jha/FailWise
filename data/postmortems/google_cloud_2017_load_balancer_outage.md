# Google Cloud HTTP(S) Load Balancer Outage (2017)

**Company:** Google Cloud
**Year:** 2017
**Severity:** P1
**Category:** Configuration management failure

## Timeline
On April 5, 2017 between 01:13 PDT and 01:35 PDT, Google Cloud HTTP(S) Load Balancers experienced approximately a 25% error rate, with some recently modified load balancers seeing 100% failures. Clients received HTTP 502 errors during the incident. Google engineers were paged at 01:22 PDT and identified issues related to the load balancer configuration update system. At 01:34 PDT, engineers switched the configuration update process to a different master server, which mitigated most of the impact within one minute. Configuration updates were paused for several hours while engineers investigated the root cause.

## Root Cause
The outage was caused by a bug in the HTTP(S) Load Balancer configuration update system. One replica of the master configuration server lost access to Google’s distributed file system and could not read recent configuration files. When leadership transferred to this outdated replica, it attempted to deploy a stale configuration globally after a failed test rollout. This rollback triggered large-scale garbage collection on Google Frontend servers because many configurations appeared deleted. Excessive garbage collection consumed significant CPU resources, causing health check failures and server restarts that resulted in HTTP 502 errors.

## Resolution
Google engineers manually redirected configuration management to a healthy master server and paused all configuration pushes while the issue was investigated. Once configuration consistency was restored, affected frontend servers stabilized and error rates returned to normal. Engineers also temporarily halted HTTP(S) Load Balancer configuration changes until the underlying issue was fully understood.

## Learnings
Google implemented several safeguards following the incident. Master servers were updated to reject outdated configuration pushes, and Google Frontend servers were modified to refuse stale configuration files. The company also improved testing for configuration deployments, fixed the distributed file system access issue that triggered the failure, and strengthened frontend health-check behavior during heavy garbage collection events.