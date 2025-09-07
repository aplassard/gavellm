from pathlib import Path

from gavellm.core.prompt import PromptTemplate


def test_prompt_render(tmp_path: Path):
    path = tmp_path / "p.yaml"
    path.write_text("""id: x
version: '1'
system: hello
user: world {{ name }}
""")
    tmpl = PromptTemplate.load(path)
    rendered = tmpl.render(name="Bob")
    assert "world Bob" in rendered
