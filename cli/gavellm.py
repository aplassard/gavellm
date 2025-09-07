from __future__ import annotations

from pathlib import Path
import sys

import typer

ROOT = Path(__file__).resolve().parents[1] / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gavellm.core.types import Case, JudgeMode
from gavellm.io.jsonl import load_cases, write_judgments
from gavellm.tasks.format_compliance import FormatComplianceTask
from gavellm.tasks.groundedness import GroundednessTask

app = typer.Typer()

TASKS = {
    "groundedness": GroundednessTask,
    "format": FormatComplianceTask,
}


@app.command()
def judge(
    task: str = typer.Option(..., help="Task name"),
    cases: Path = typer.Option(..., help="Path to cases JSONL"),
    mode: JudgeMode = typer.Option(JudgeMode.RULES_ONLY, help="Judging mode"),
    out: Path = typer.Option(Path("out.judgments.jsonl"), help="Output JSONL path"),
) -> None:
    task_cls = TASKS[task]
    t = task_cls(mode)
    judgments = [t.judge(c) for c in load_cases(cases)]
    write_judgments(out, judgments)


if __name__ == "__main__":
    app()
