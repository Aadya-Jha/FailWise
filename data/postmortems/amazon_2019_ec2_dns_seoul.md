# Cloudflare Backbone Outage (2020)

**Company:** Cloudflare
**Year:** 2020
**Severity:** P1
**Category:** Network outage

## Timeline
At 20:25 UTC, a backbone link between Newark and Chicago failed, causing congestion between Atlanta and Washington DC. During mitigation efforts, a configuration change was made on an Atlanta router at 21:12 UTC. This accidentally redirected global backbone traffic to Atlanta, overwhelming the router and causing outages across multiple Cloudflare regions. Service was restored between 21:39 and 21:47 UTC after the Atlanta router was removed from the backbone. Full recovery, including logs and metrics systems, completed by 22:10 UTC.

## Root Cause
The outage was caused by a configuration mistake during backbone traffic mitigation. Engineers intended to deactivate a routing policy term but instead removed a prefix-list condition. This caused all BGP routes to be advertised with a higher local preference, making Atlanta attract traffic from across the backbone network. The Atlanta routers became overloaded, leading to widespread service disruption.

## Resolution
Engineers identified the faulty routing behavior and removed the Atlanta router from the backbone network. Traffic flow normalized shortly afterward, restoring affected services. Additional monitoring was performed to recover internal logging and metrics systems.

## Learnings
Cloudflare implemented safeguards to prevent similar routing mistakes in the future. They introduced maximum-prefix limits on backbone BGP sessions and adjusted local-preference settings to prevent a single location from attracting excessive traffic. The company also reviewed operational procedures around configuration changes and backbone routing safety.