# Agent Line Map: Cortex PM Chief-of-Staff Agent

> Module 1 · The Agent Line
>
> ✅ **What this validates:** every risky action has a clear owner, by the end you'll have proven an above/below-the-line map with HITL checkpoints, scored on reversibility, blast radius, and measurability.

## The workflow, decision by decision

List every discrete decision or action in your agent's workflow, then score each one and place it **above** the line (a human owns it) or **below** (the agent owns it). Borderline calls get an HITL checkpoint.

| Decision / action | Reversibility (H/M/L) | Blast radius (H/M/L) | Measurability (H/M/L) | Above / Below | HITL? |
|---|---|---|---|---|---|
| Pull project state + activity | H | L | H | Below | · |
| Decide relevant context | H | M | M | Below | required |
| Draft the update | H | L | M | Below | · |
| Decide tone/commitment level | M | M | L | Above | · |
| Flag at-risk/escalation | H | L | M | Below | · |
| Choose what to escalate | M | H | L | Below | required |
| Propose a story batch (capped) | H | L | H | Below | · |
| Post an update / approve a company-wide one | L | H | M | Above | · |

## Agent anatomy (sketch)

- **Model:** gpt-4o-mini by default; escalates to gpt-4o for tone/commitment-level calls
- **Tools:** project + activity lookup (read) · past-update search · roadmap · team norms · story proposal (capped) · notification tool (for HITL steps)
- **Memory:** roadmap and team norms persist across runs; raw pulled activity data is purged after each run
- **Loop:** _placeholder, defined in M2 loop-spec.md_
- **Bounds:** _placeholder, defined in M5 bounds-and-evals.md_
- **Evals:** _placeholder, defined in M5 bounds-and-evals.md_

## The golden rule, applied

1. Pull project state + activity sits below the line because it's high to reverse, has a low blast radius, and is high to verify — deciding factor: blast radius.
2. Decide relevant context sits below the line (HITL required) because it's high to reverse, has a medium blast radius, and is medium to verify — deciding factor: measurability.
3. Draft the update sits below the line because it's high to reverse, has a low blast radius, and is medium to verify — deciding factor: blast radius.
4. Decide tone/commitment level sits above the line because it's medium to reverse, has a medium blast radius, and is low to verify — deciding factor: measurability.
5. Flag at-risk/escalation sits below the line because it's high to reverse, has a low blast radius, and is medium to verify — deciding factor: blast radius.
6. Choose what to escalate sits below the line (HITL required) because it's medium to reverse, has a high blast radius, and is low to verify — deciding factor: blast radius.
7. Propose a story batch (capped) sits below the line because it's high to reverse, has a low blast radius, and is high to verify — deciding factor: blast radius.
8. Post an update / approve a company-wide one sits above the line because it's low to reverse, has a high blast radius, and is medium to verify — deciding factor: reversibility.

## Hardest call

**Decide relevant context.** First instinct was Below (a cheap-to-reverse judgment call), but scoring it exposed the real problem: measurability. It's hard to tell after the fact whether Cortex picked the *right* context, and a wrong pick quietly biases everything drafted downstream without leaving an obvious trace. Measurability is what tipped it to HITL — Cortex still does the work, but a human spot-checks the context selection before it feeds the draft.
