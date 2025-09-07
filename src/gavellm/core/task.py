from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

from .types import Case, Judgment, JudgeMode


class JudgeTask(ABC):
    """Base class for all judge tasks."""

    def __init__(self, mode: JudgeMode):
        self.mode = mode

    @abstractmethod
    def _rules(self, payload: Dict[str, Any]) -> Tuple[bool | None, Dict[str, Any]]:
        """Return (decision, details). Decision ``None`` means inconclusive."""

    @abstractmethod
    def _llm(self, payload: Dict[str, Any]) -> Judgment:
        """LLM-based judging implementation."""

    def judge(self, case: Case) -> Judgment:
        decision, details = self._rules(case.payload)
        if self.mode == JudgeMode.RULES_ONLY:
            pass_fail = bool(decision)
            return Judgment(case.id, pass_fail, scores=details.get("scores", {}), explanation=details.get("explanation", ""), raw=details)
        if self.mode == JudgeMode.LLM_ONLY:
            return self._llm({**case.payload, "id": case.id})
        # HYBRID
        if decision is not None:
            return Judgment(case.id, bool(decision), scores=details.get("scores", {}), explanation=details.get("explanation", ""), raw=details)
        return self._llm({**case.payload, "id": case.id})
