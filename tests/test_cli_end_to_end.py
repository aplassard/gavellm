from pathlib import Path
import json

import subprocess


def test_cli_groundedness(tmp_path: Path):
    out = tmp_path / "out.jsonl"
    subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "cli.gavellm",
            "--task",
            "groundedness",
            "--cases",
            "tasks/groundedness.sample.jsonl",
            "--mode",
            "RULES_ONLY",
            "--out",
            str(out),
        ],
        check=True,
    )
    lines = out.read_text().strip().splitlines()
    assert len(lines) == 5
    for line in lines:
        json.loads(line)
