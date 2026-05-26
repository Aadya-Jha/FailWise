# CircleCI Kubernetes Networking Incident (2023)

**Company:** CircleCI
**Year:** 2023
**Severity:** P1
**Category:** Kubernetes networking failure

## Timeline
On March 14, 2023 at approximately 18:00 UTC, CircleCI customers began experiencing severe delays in starting jobs and running pipelines. As the incident progressed, pipelines stopped executing entirely and job queues rapidly backed up across multiple services. Engineers investigated widespread service-to-service communication failures within CircleCI’s primary Kubernetes production cluster. Between 20:00 and 21:00 UTC, attempts to restart DNS-related services worsened the outage and caused complete DNS resolution failures. By 23:00 UTC, large-scale node restarts began restoring networking functionality, and full job execution recovery completed around 01:27 UTC on March 15. Additional RabbitMQ-related recovery incidents caused further delays until approximately 13:15 UTC.

## Root Cause
The incident was caused by a Kubernetes upgrade that introduced a version mismatch between kubelet and kube-proxy components. During rollback and upgrade operations, kube-proxy generated repeated iptables synchronization failures while attempting to reconcile routing rules for Kubernetes Services and Endpoints. These failures corrupted iptables state across multiple nodes, causing widespread networking instability and service-to-service communication failures throughout the cluster. Subsequent remediation actions exposed additional weaknesses in RabbitMQ queue infrastructure, leading to secondary incidents during recovery.

## Resolution
CircleCI engineers investigated networking failures across kube-proxy, CoreDNS, and node-local DNS cache components before identifying kube-proxy synchronization failures as the primary issue. Teams restarted nodes across the production cluster, rebuilding iptables state and restoring networking functionality. Additional infrastructure rollouts and RabbitMQ restarts were performed to stabilize queues and recover delayed GitHub checks. Monitoring continued after services recovered to ensure queue backlogs and networking behavior returned to normal.

## Learnings
CircleCI enhanced Kubernetes upgrade procedures to reduce the risk of similar version mismatch failures and added new observability metrics and alerts specifically targeting kube-proxy synchronization errors. The company also began evaluating strategies to improve RabbitMQ resilience and acknowledged that foundational infrastructure upgrades require stronger risk mitigation and recovery planning due to their broad system impact.