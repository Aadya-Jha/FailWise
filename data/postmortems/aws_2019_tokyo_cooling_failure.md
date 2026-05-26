# AWS Tokyo EC2 and EBS Cooling Failure (2019)

**Company:** AWS
**Year:** 2019
**Severity:** P1
**Category:** Datacenter infrastructure failure

## Timeline
On August 23, 2019 at 12:36 PM JST, a portion of a single Availability Zone in the AWS Tokyo (AP-NORTHEAST-1) region experienced overheating that caused some EC2 servers to shut down unexpectedly. This led to impaired EC2 instances, degraded EBS performance, snapshot creation failures, and issues with the EC2 RunInstances API and Auto Scaling. Cooling systems were restored by 3:21 PM JST, after which temperatures gradually normalized and power was restored to affected infrastructure. By 6:30 PM JST, most impacted EC2 instances and EBS volumes had recovered, although some hardware permanently failed due to heat and power-related damage.

## Root Cause
The incident was caused by a failure in AWS’s datacenter control system responsible for managing cooling infrastructure. During a failover between control hosts, a bug in third-party control system logic caused excessive communication with cooling equipment and Programmable Logic Controllers (PLCs), making both the control system and some PLCs become unresponsive. In affected parts of the datacenter, cooling systems failed to enter safe maximum-cooling mode and instead shut down entirely. Attempts to activate emergency “purge mode” also failed because the PLC controllers were unresponsive, causing temperatures to rise until servers automatically powered off to prevent hardware damage.

## Resolution
AWS engineers manually investigated and reset the affected cooling systems and PLC controllers to restore cooling functionality. Once temperatures stabilized, power was restored to impacted servers and storage systems. Engineers also resolved issues affecting the EC2 RunInstances API and Auto Scaling functionality during recovery. Some damaged hardware required retirement and replacement before all affected instances and volumes could fully recover.

## Learnings
AWS disabled the control-system failover mode that triggered the bug while continuing investigation with third-party vendors. The company also trained operations teams to recognize and remediate similar failures more quickly in the future. Additionally, AWS began redesigning cooling system controls so emergency purge mode could bypass PLC controllers entirely, improving resilience against future controller failures. AWS also reiterated the importance of deploying applications across multiple Availability Zones for high availability.