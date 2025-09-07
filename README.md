# gavellm

Open source LLM-as-a-judge.

## Development

This project uses [uv](https://github.com/astral-sh/uv) for Python dependency
management. To get started:

1. Install uv. The recommended method is:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   or see the [uv docs](https://docs.astral.sh/uv/) for other options.
2. Install dependencies and create the virtual environment:
   ```bash
   uv sync
   ```
3. Run commands through uv:
   ```bash
   uv run python -m pytest  # run tests
   ```

Project code lives in `src/gavellm/`.

## Usage

Two starter judge tasks are provided:

* **Groundedness** – determine whether an answer is supported by context snippets.
* **Format compliance** – check if a candidate output follows structural constraints.

Run judgments via the CLI:

```bash
uv run python -m cli.gavellm \
  --task groundedness \
  --cases tasks/groundedness.sample.jsonl \
  --mode RULES_ONLY \
  --out out/groundedness.jsonl
```

Sample cases for each task live in `tasks/` and prompts in `prompts/`.
