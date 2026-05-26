# Zerodha OMS Overload Incident (2019)

**Company:** Zerodha
**Year:** 2019
**Severity:** P1
**Category:** Order management system failure

## Timeline
On August 29, 2019 between 10:00 AM and 10:40 AM, Zerodha experienced a major issue affecting its Order Management System (OMS). During the outage, clients were unable to place new orders. Although order placement functionality was restored after 10:40 AM, customers with open orders executed during the affected period experienced incorrect additional margin blocks until Zerodha reconciled positions with the exchanges. The issue was traced back to an unusually fragmented trade execution pattern originating from a single large order placed earlier in the trading session.

## Root Cause
The incident was triggered by a single order for 10 lakh shares of a penny stock on the Bombay Stock Exchange. Instead of executing in the usual few hundred trades, the exchange matched the order across more than 1 lakh individual trades. This unprecedented execution pattern overwhelmed the OMS infrastructure provided by Refinitiv (formerly Thomson Reuters). The OMS was not designed to handle such an extreme number of trade fragments from a single order, causing processing overload and disruption to order placement services.

## Resolution
Zerodha and Refinitiv investigated the OMS overload and restored order placement services after approximately 40 minutes. To reduce the risk of recurrence before a permanent OMS fix was developed, Zerodha introduced a temporary limit of 20,000 shares per equity order. Customers needing larger quantities were instructed to split trades across multiple orders. Zerodha also planned to introduce basket order functionality to simplify multi-order execution for large trades.

## Learnings
The incident highlighted the risks posed by rare market liquidity edge cases and unexpected exchange execution behavior. Zerodha and Refinitiv began working on OMS improvements capable of handling extremely fragmented order executions. The company also introduced operational safeguards through temporary order-size limits and emphasized the importance of designing financial infrastructure for unusual high-volume execution scenarios.