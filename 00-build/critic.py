"""Independent validator (M3). A separate model call that never saw the drafting
context, so it can't inherit the draft's blind spots. Returns a pass/fail verdict.
The revision cap that stops a critic<->drafter loop lives in `agent.py`.
"""

from __future__ import annotations

import json
import re

from prompts import CRITIC_SYSTEM


def _extract_json(text: str) -> dict:
    """Anthropic has no strict JSON mode, so Claude sometimes wraps the object in
    markdown fences or a sentence. Try a straight parse, then fall back to pulling
    out the first {...} block before giving up."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return {"verdict": "fail", "reasons": ["critic returned unparseable output"]}


def review(client, model: str, proposed_output: str, source_data: str) -> dict:
    """Return {"verdict": "pass"|"fail", "reasons": [...]} for a proposed output."""
    resp = client.messages.create(
        model=model,
        max_tokens=1024,
        system=CRITIC_SYSTEM,
        messages=[
            {"role": "user", "content":
                f"SOURCE DATA Cortex used:\n{source_data}\n\n"
                f"CORTEX PROPOSED OUTPUT:\n{proposed_output}\n\n"
                "Respond with ONLY the JSON object, no markdown fences, no other text."},
        ],
    )
    usage = resp.usage
    text = "".join(b.text for b in resp.content if b.type == "text")
    verdict = _extract_json(text)
    verdict["_usage"] = {"prompt": usage.input_tokens, "completion": usage.output_tokens}
    return verdict
