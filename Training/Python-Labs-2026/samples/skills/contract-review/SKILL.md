---
name: contract-review
description: Classify vendor contract renewal risk from contract text the user provides.
allowed-tools: Read
---
Read the contract the user supplies. Compute the cancellation deadline (end date minus notice days),
then classify risk as HIGH, MEDIUM or LOW using the team's risk rule. Return a short table.
