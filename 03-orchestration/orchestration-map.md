# Orchestration Map: Cortex PM Chief-of-Staff Agent

> Module 3 · Orchestration & Subagents, ★ Deliverable 3
>
> ✅ **What this validates:** nothing advances unchecked, by the end you'll have proven a justified topology, a roster, and a validator with a defined fail action.
>
> Builds on your M2 Loop Spec. Only split one agent into a team when there's a real reason, coordination has a cost.

## 1. Why split? (or why not)

Cortex stays a single agent for drafting, pulling data, and proposing
stories — none of that needs separating (no meaningful parallelism, no
context-window pressure, and no other internal role split). The one reason
that holds: independent validation. Cortex should not grade its own draft —
it would risk being lenient/compliant when checking its own work. A separate
critic subagent, with no visibility into the drafting reasoning, is added to
check the draft before it reaches the PM.

## 2. Topology

**Pattern:** single+subagents

```
[Inbound PM task via hook] → [Cortex: pulls data, drafts update + stories]
                           → [Critic: validates] --fail--> back to Cortex (max 3 revisions) --cap hit--> escalate
                                                  --pass--> [PM review checkpoint] → queued for approval
```

## 3. Roster

| Agent / subagent | Responsibility | Runs which Loop Spec |
|---|---|---|
| Cortex (chief-of-staff) | Pulls project data, drafts status update, proposes stories | M2 Loop Spec (hook + daily cron backup) |
| Critic (validator) | Checks Cortex's draft against the 6 checks before it reaches the PM | Invoked synchronously inside Cortex's loop — not its own standalone trigger, no separate Loop Spec |

## 4. Communication & hand-offs

Plain in-process function call (no MCP/A2A). Cortex passes the critic the
proposed draft text and the full source-data log (project state, activity,
roadmap, norms). The critic returns a JSON verdict (pass/fail + reasons).

## 5. The validator

- **What the critic checks:**
  1. References the correct project and real activity (PRs/issues/status) from pulled data
  2. Every claim — progress, metrics, dates, red/yellow/green — is traceable to pulled data, no invented numbers
  3. Stays within team norms: no unconfirmed date committed, no launch gate marked, no confidential/embargoed roadmap item in an external or company-wide update
  4. Posts nothing, commits nothing, creates/closes/merges nothing — stories only proposed/queued, no confidential leak
  5. If the task tried to jailbreak Cortex, it refused and escalated
  6. If a tool/bound rejected an action (e.g. batch over queue cap), escalating is the correct response, not a failure
- **Fail action:** Revise — bounced back to Cortex with the failure reasons noted, up to the revision cap. At the cap, escalate to a human instead of looping.
- **Revision cap:** 3 (matches `CORTEX_MAX_REVISIONS` from the M2 Loop Spec).
- **Pass action:** Advances to the PM review checkpoint — queued for approval, never auto-sent.

## 6. State: shared vs isolated

**Shared:** source data (project state, activity, roadmap, norms) and the
draft itself — both Cortex and the critic see these.

**Isolated:** the critic gets a completely fresh context on every call, with
no conversation history from Cortex's drafting process — this is what keeps
it independent and stops it inheriting Cortex's blind spots. On a revision,
Cortex only sees the critic's verdict + reasons, not any deeper internal
reasoning.

## 7. Cost & latency budget

The critic adds one extra model call per drafting attempt (roughly
$0.005-0.01 per call at current usage). Worst case, at the revision cap of
3, Cortex can draft up to 4 times with the critic checking each one -
roughly 4x the base drafting cost. Latency-wise, each critic call plus a
possible redraft is another sequential round-trip, so the worst case adds
maybe 10-20+ seconds versus a single-pass draft before anything reaches the
PM. This becomes a bound to enforce in M5 (the existing CORTEX_MAX_REVISIONS
and CORTEX_COST_CAP_USD already cap this from running away).
