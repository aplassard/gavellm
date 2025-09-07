from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict

from gavellm.core.prompt import PromptTemplate
from gavellm.core.task import JudgeTask
from gavellm.core.types import Judgment, JudgeMode
from gavellm.llm import chat_completion
from gavellm.rules.groundedness import check_groundedness

PROMPT_PATH = Path(__file__).resolve().parents[3] / "prompts" / "groundedness.yaml"


class GroundednessTask(JudgeTask):
    def __init__(self, mode: JudgeMode):
        super().__init__(mode)
        self.template = PromptTemplate.load(PROMPT_PATH)

    def _rules(self, payload: Dict[str, Any]):
        result = check_groundedness(payload["context_snippets"], payload["answer"])
        decision = None
        if result["support_ratio"] in {0.0, 1.0}:
            decision = result["supported"]
        return decision, {"scores": {"support_ratio": result["support_ratio"]}, **result}

    def _llm(self, payload: Dict[str, Any]) -> Judgment:
        prompt = self.template.render(**payload)
        resp = chat_completion(prompt)["message"]
        data = _parse_json(resp)
        return Judgment(
            case_id=payload.get("id", ""),
            pass_fail=bool(data.get("supported")),
            scores={"support_ratio": data.get("support_ratio", 0.0)},
            explanation=data.get("explanation", ""),
            raw=data,
        )


def _parse_json(text: str) -> Dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group())
        raise
