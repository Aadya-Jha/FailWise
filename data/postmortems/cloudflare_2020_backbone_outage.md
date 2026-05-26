# Cloudflare backbone outage (July 2020)

**Company:** Cloudflare
**Year:** 2020
**Severity:** P1
**Category:** Network Outage

## Timeline
On July 17, 2020 a configuration error in our backbone network caused an outage for Internet properties and Cloudflare services that lasted 27 minutes. We saw traffic drop by about 50% across our network. Because of the architecture of our backbone this outage didn’t affect the entire Cloudflare network and was localized to certain geographies.

## Root Cause
The outage occurred because, while working on an unrelated issue with a segment of the backbone from Newark to Chicago, our network engineering team updated the configuration on a router in Atlanta to alleviate congestion. This configuration contained an error that caused all traffic across our backbone to be sent to Atlanta. This quickly overwhelmed the Atlanta router and caused Cloudflare network locations connected to the backbone to fail. First, an issue occurred on the backbone link between Newark and Chicago which led to backbone congestion in between Atlanta and Washington, DC. Shortly after, we saw congestion at one of our core data centers that processes logs and metrics, causing some logs to be dropped. During this period the edge network continued to operate normally.

## Resolution
Shortly after, we saw congestion at one of our core data centers that processes logs and metrics, causing some logs to be dropped. During this period the edge network continued to operate normally.
{master}[edit]
atl01# show | compare 
[edit policy-options policy-statement 6-BBONE-OUT term 6-SITE-LOCAL from]
!       inactive: prefix-list 6-SITE-LOCAL { ... }
The complete term looks like this:

from {
    prefix-list 6-SITE-LOCAL;
}
then {
    local-preference 200;
    community add SITE-LOCAL-ROUTE;
    community add ATL01;
    community add NORTH-AMERICA;
    accept;
}


## Learnings
We are taking multiple steps to prevent recurrence of this issue, some of which are already complete. We have immediately validated and ensured that every AWS region has the correct capacity settings for the EC2 DNS resolver service. We are implementing semantic configuration validation for all EC2 DNS resolver configuration updates, to ensure every region always has sufficient minimum healthy hosts. We are also adding throttling to ensure that only a limited amount of healthy host capacity can be removed from service each hour. This will prevent the downscaling of the EC2 DNS resolver fleet in the event of an invalid configuration parameter.