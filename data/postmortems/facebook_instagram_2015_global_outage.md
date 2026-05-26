# Facebook and Instagram Global Outage (2015)

**Company:** Facebook
**Year:** 2015
**Severity:** P0
**Category:** Network configuration failure

## Timeline
On January 26, 2015 at approximately 10:10 PM Pacific Time, Facebook experienced a major global outage that lasted for about one hour. During the outage, Facebook services became unreachable as TCP connections timed out and packet loss exceeded 80% across Facebook’s network. Instagram, which was hosted separately on AWS infrastructure, also became unavailable but continued accepting TCP connections while returning HTTP 503 errors. Around 11:05 PM Pacific Time, Facebook began restoring network connectivity, and full service recovered by approximately 11:20 PM.

## Root Cause
According to Facebook’s statements, the outage was triggered by a configuration system change. Network analysis suggested that traffic inside Facebook’s datacenters was blocked before reaching production servers, likely due to an incorrect Access Control List (ACL) or internal routing configuration. Packets were dropped within Facebook’s aggregation layer, causing widespread connection failures across Facebook’s core infrastructure.

## Resolution
Facebook engineers isolated the faulty configuration and restored normal network routing behavior inside affected datacenters. TCP connectivity gradually returned first, followed by full application-level recovery. Instagram services recovered separately after backend dependencies stabilized.

## Learnings
The incident highlighted the risks associated with large-scale configuration changes in globally distributed networks. It reinforced the importance of staged rollouts, stronger safeguards around ACL and routing updates, and better isolation between configuration management systems and production traffic paths. The outage also demonstrated how separate infrastructure architectures, such as Instagram’s AWS hosting, can experience different failure characteristics during shared backend incidents.