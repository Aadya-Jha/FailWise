# Google Cloud Networking Packet Loss Incident (2022)

**Company:** Google Cloud
**Year:** 2022
**Severity:** P1
**Category:** Network failure

## Timeline
On May 20, 2022 at 13:47 US/Pacific, Google Cloud Networking experienced intermittent packet loss affecting inter-region traffic across multiple global cloud regions. Customers observed elevated latency, timeouts, HTTP 500 errors, routing delays, and connectivity issues across services including Cloud VPN, Cloud Storage, Cloud SQL, and Cloud Interconnect. Google’s automated network repair systems rerouted traffic through alternate backbone paths, and the issue was fully mitigated by 14:07 US/Pacific. A detailed incident report was later published on June 2, 2022.

## Root Cause
The incident was caused by a failure of an optical amplification component on a fiber path connected to a central US gateway campus within Google’s production backbone network. The failure reduced available bandwidth between backbone gateways and edge locations, causing packet loss during automatic traffic rerouting. The network topology in the affected region was undergoing augmentation, and the preferred secondary failover path was incomplete. As a result, traffic had to reroute through a less optimal tertiary path, significantly increasing convergence time and prolonging the disruption.

## Resolution
Google’s automated repair and rerouting systems detected the bandwidth reduction and automatically shifted traffic onto alternate network paths. Traffic convergence completed within approximately 20 minutes, restoring normal connectivity without requiring manual intervention. Engineers continued monitoring affected services while remediation plans for the underlying network topology were developed.

## Learnings
Google identified the need to further optimize network convergence times and improve resilience during topology augmentation. The company committed to completing network augmentation work in the affected region and implementing automated analysis systems to ensure temporary network topologies still support rapid failover. Additional efforts were also planned to reduce the severity and duration of future backbone rerouting events.