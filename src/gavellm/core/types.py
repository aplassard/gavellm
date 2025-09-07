from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict


class JudgeMode(str, Enum):
    """Execution strategy for a judge task."""

    RULES_ONLY = "RULES_ONLY"
    LLM_ONLY = "LLM_ONLY"
    HYBRID = "HYBRID"


@dataclass
class Case:
    """A single example to judge."""

    id: str
    payload: Dict[str, Any]


@dataclass
class Criterion:
    """Description of what is being evaluated."""

    name: str
    description: str


@dataclass
class Judgment:
    """Result from judging a :class:`Case`."""

    case_id: str
    pass_fail: bool
    scores: Dict[str, float] = field(default_factory=dict)
    explanation: str = ""
    raw: Dict[str, Any] | None = None
