from __future__ import annotations

import json
import re
from typing import Dict, List

import jsonschema


def check_format(constraints: Dict[str, object], candidate: str) -> Dict[str, object]:
    violations: List[str] = []
    if "banned_phrases" in constraints:
        for phrase in constraints["banned_phrases"]:
            if phrase in candidate:
                violations.append(f"contains banned phrase '{phrase}'")
    if "regex" in constraints:
        for desc, pattern in constraints["regex"].items():
            if not re.search(pattern, candidate):
                violations.append(f"missing pattern '{desc}'")
    if "json_schema" in constraints:
        try:
            data = json.loads(candidate)
            jsonschema.validate(data, constraints["json_schema"])
        except Exception as exc:  # pragma: no cover - simplified handling
            violations.append(f"json_schema: {exc}")
    if "required_count" in constraints:
        target = constraints["required_count"]
        word = target.get("word")
        count = target.get("count", 0)
        if candidate.count(word) < count:
            violations.append(f"expected at least {count} occurrences of '{word}'")
    result = {
        "compliant": not violations,
        "violations": violations,
    }
    result["explanation"] = "; ".join(violations) if violations else "compliant"
    return result
