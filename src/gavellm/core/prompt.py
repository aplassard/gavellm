from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, StrictUndefined


@dataclass
class PromptTemplate:
    """Load and render system/user prompt templates."""

    id: str
    version: str
    system: str
    user: str

    @classmethod
    def load(cls, path: Path) -> "PromptTemplate":
        data = yaml.safe_load(path.read_text())
        return cls(**data)

    def render(self, **kwargs: Any) -> str:
        env = Environment(undefined=StrictUndefined)
        system_t = env.from_string(self.system)
        user_t = env.from_string(self.user)
        system = system_t.render(**kwargs)
        user = user_t.render(**kwargs)
        return f"{system}\n\n{user}"
