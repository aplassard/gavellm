from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from gavellm.core.types import Case, Judgment


def load_cases(path: Path) -> List[Case]:
    cases = []
    with path.open() as f:
        for line in f:
            data = json.loads(line)
            case_id = data.pop("id")
            cases.append(Case(id=case_id, payload=data))
    return cases


def write_judgments(path: Path, judgments: Iterable[Judgment]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for j in judgments:
            f.write(json.dumps(j.__dict__) + "\n")
