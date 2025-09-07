from __future__ import annotations

import re
from typing import Dict, List


def check_groundedness(context_snippets: List[str], answer: str) -> Dict[str, object]:
    sentences = [s.strip() for s in re.split(r"[\.?!]", answer) if s.strip()]
    supported = []
    missing = []
    for sent in sentences:
        if any(sent.lower() in ctx.lower() for ctx in context_snippets):
            supported.append(sent)
        else:
            missing.append(sent)
    ratio = len(supported) / len(sentences) if sentences else 0.0
    result = {
        "supported": ratio == 1.0 if sentences else False,
        "support_ratio": ratio,
        "missing_citations": missing,
    }
    if missing:
        result["explanation"] = f"Missing support for: {missing}"
    else:
        result["explanation"] = "All claims supported." if sentences else "No answer given."
    return result
