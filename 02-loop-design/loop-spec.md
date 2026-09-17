# Loop Spec: Cortex PM Chief-of-Staff Agent

> Module 2 · Loop Engineering, ★ Deliverable 2
>
> ✅ **What this validates:** the agent knows when to run and when to stop, by the end you'll have proven a one-page Loop Spec with a trigger, a definition of "done," and explicit stop conditions.
>
> Your one-page blueprint for how the work you handed to the agent (M1) actually *runs*.
> An agent is just a prompt that fires itself, this spec says when it fires, what "done" means, and what it needs to do the job. Living document; refine as the course progresses.

## 1. Trigger & loop type

**Chosen type:** Hook (primary), with a daily cron sweep as backup

Why this type? Cortex's job is triggered by demand — someone asks for a status
update — so a hook that fires on the inbound request message is the natural
primary trigger. A daily cron sweep acts as a safety net: if the hook didn't
fire that day (missed event, delivery failure), the cron catches it so an
update never silently goes missing.

Ruled out — Heartbeat: polling on a fixed interval doesn't make sense here;
the underlying project data doesn't shift often enough to justify checking on
a timer. Ruled out — Goal: this loop is a data-pull-and-draft refresh, not a
self-validating goal-seeking process; a goal loop belongs to a separate
drafting/validation agent, not this data refresh.

Idempotency: hook fires keyed on message ID; a duplicate delivery of the same
message ID is deduped and does not trigger a second draft.

## 2. Goal / definition of done

Draft written and queued for approval; Cortex never sends. Success requires
all required project data to be pulled and a draft that passes the
independent validator's (critic's) content-quality checks.

## 3. Stop conditions

| Condition | What it looks like | What happens |
|---|---|---|
| **Success** | All required data pulled; draft approved by the validator on content quality | Loop halts; draft queued for human review, nothing sent |
| **Stuck / give up** | Data cannot be pulled after 3 attempts, OR the draft is not accepted by the validator after 3 revision attempts | Escalate + log; halt the loop |
| **Escalate to human** | An embargoed/confidential roadmap item surfaces, a tone/commitment call is needed, or the proposed story batch exceeds the queue cap | HITL checkpoint (from agent-line-map.md) |

## 4. State

Persists across iterations: the last processed message ID per project (for
hook dedupe) and the last drafted status update per project. Scope is
strictly per-project — confidential/embargoed roadmap items for one project
must never leak into another project's context or draft.

## 5. The five things a loop can lean on

_`state` is always-on. `connectors` only if you already have one wired (e.g. a Jira key or Google MCP), otherwise just note it as a plan. `skills`, `subagents`, `work tree` scale with autonomy; "not needed yet, because…" is a valid answer._

| Component | For Cortex |
|---|---|
| **Work tree** (isolated workspace per run, a git worktree) | Not needed yet, because there are no race conditions or overlapping runs right now. |
| **Skills** (reusable capabilities) | Not needed yet — they'll be created as the agents are refined. |
| **Plugins / connectors** (tools & access, optional if you don't have one yet) | Not wired yet, still a plan. Today all tools are mock fixtures in `00-build/fixtures/`. |
| **Subagents** (independent check when the loop can't grade itself) | placeholder → M3 orchestration-map.md |
| **State tracking** | Locked on — see §4. |

> Context plan (M4) and the hand-off to bounds & evals (M5) come in later modules, you'll add them to their own deliverables then, not here.

## Link to live loop

_[path to your agent in `00-build/`]_
