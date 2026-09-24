# Context Engineering & Memory: Cortex PM Chief-of-Staff Agent

> Module 4 · Context Engineering & Memory
>
> ✅ **What this validates:** the agent reasons on the right, safe inputs, by the end you'll have proven a context budget, per-source retrieve-vs-long-context decisions, and a memory map with risk mitigations.
>
> 🗂️ **How the lab maps to this file:** In **Part A** (before the lecture) you don't edit this file, you rough-draft on scratch, focused on the per-source calls in **section 2** plus a quick remember/forget + "how it rots" sketch. In **Part B** (after the lecture) you complete **all five sections**; the Lab Guide's guided builder writes this file for you to copy in and commit.

## 1. Context budget

Priority order (what must never get dropped, even under budget pressure, vs.
what's sized to fit):

1. **Task brief** (long-context, always) — anchors what's actually being asked.
2. **Confidentiality rule** from team norms (pinned, always) — the one rule
   that can never be silently missed by a relevance-based retrieval.
3. **Full roadmap** (long-context, always) — needs the whole document, flags
   included, for Cortex to correctly audit what must stay out of an update.
4. **Rest of the norms guide** (retrieved, scoped to the current task) — the
   guide will keep growing, so only the relevant style/process rules for
   this situation are pulled in.
5. **Project activity** (retrieved, scoped to the one project in the task) —
   this grows unbounded over a project's life and goes stale fast.
6. **Past-updates precedent** (retrieved, most relevant/latest only) — an
   unbounded, ever-growing corpus; only recent tone/format precedent matters.

## 2. Retrieve vs. long-context: per source

For each data source, decide: **retrieve** (narrow a large/changing corpus to the relevant slice) or **long-context** (just include a bounded set you can reason over).

| Source | Size / volatility | Decision | Why |
|---|---|---|---|
| `get_task` (task brief) | One static doc, bounded | Long-context | Nothing to search; reason over the whole thing (size) |
| `get_roadmap` | Medium, has confidential flags | Long-context | Must audit the entire doc, including flags — a filtered slice risks missing a confidential item (citation/audit) |
| `get_norms` | Medium, grows over time | Hybrid | Confidentiality rule pinned/always-included (citation/audit); rest retrieved by use-case relevance as the guide grows (size/volatility) |
| `get_activity` | Grows unbounded per project | Retrieve | Changes constantly and only grows over a project's life (volatility) |
| `search_past_updates` | Unbounded corpus | Retrieve | Dumping the whole history would blow the budget; only the latest relevant precedent matters (size) |

## 3. Retrieval quality plan

| Source | Failure mode | Agentic move(s) | Why |
|---|---|---|---|
| `get_activity` | Not wrong-document risk (direct lookup) — risk is Cortex overstating/embellishing what activity actually shows | Self-verification | Every claim in the draft must trace back to what the tool actually returned (no invented metrics or progress) |
| `search_past_updates` | Naive keyword-overlap search; falls back to the first 2 corpus items (regardless of relevance) when nothing matches | Document grading + Reranking | Grade returned precedent for actual relevance to the current project/topic before trusting it; rerank to pick the single best match when several come back |
| `get_norms` (retrieved portion) | As the norms guide grows, relevance-scoped retrieval can miss a rule that applies but doesn't share vocabulary with the query | Routing + Document grading | Route to the right section/category of the norms guide for this task type; grade a retrieved rule to confirm it actually applies before citing it |

*(`get_norms`'s pinned confidentiality rule and the two long-context sources — `get_roadmap`, `get_task` — aren't retrieved, so no agentic-retrieval move applies to them; their safety comes from being included in full, per §1/§2.)*

## 4. Memory map (your PM brain)

| Memory type | What Cortex stores | Scope / TTL |
|---|---|---|
| **Working** (in-loop) | Pulled project state, activity, roadmap, norms, draft-in-progress, critic verdict | This run only — discarded once the run ends |
| **Episodic** (past runs) | Last processed message ID per project (hook dedupe), last drafted status update per project | Persists indefinitely per-project, until overwritten by the next run for that same project |
| **Semantic** (durable facts/prefs) | Team norms, roadmap facts | Durable but not permanent — refreshed from source of truth each run (roadmap/norms can change); not separately cached by Cortex |
| **Shared** (across agents) | Source-data log + draft, passed to the critic | Lives only for the duration of one run's Cortex↔critic exchange; critic's reasoning never flows back |

## 5. Memory risks & mitigations

| Risk | Where it bites Cortex | Mitigation |
|---|---|---|
| **Drift** | If Cortex's own unapproved drafts ever fed back into `search_past_updates` as "precedent," small tone/interpretation errors could compound over time | Only human-approved, actually-published updates enter the precedent corpus — Cortex's own draft output (episodic "last drafted") stays separate and is never treated as ground-truth precedent |
| **Poisoning** | A compromised task brief (prompt injection) or a tampered fixture file could get treated as trusted ground truth | `CORTEX_SYSTEM` already treats task-brief content as data, not instructions, and flags injection attempts; Cortex has no write access to roadmap/norms (M1 agent line — read-only), so it can't be tricked into corrupting its own source of truth |
| **Staleness** | `get_activity` and the retrieved norms/precedent could go stale if cached too long | No caching on volatile sources — `get_activity` is freshly pulled every run (per §2); roadmap/norms are refreshed from source of truth each run rather than cached |
| **PII / retention** | Episodic memory (last drafted update, message IDs per project) could accumulate indefinitely, and confidential roadmap items could leak across projects if episodic state isn't scoped tightly | Per-project scope is strict (M2 §4 State) — no cross-project leakage; episodic retention gets a TTL/bound in M5 rather than growing forever |
