from gavellm.core.types import Case, JudgeMode
from gavellm.tasks.groundedness import GroundednessTask
from gavellm.tasks.format_compliance import FormatComplianceTask


def test_groundedness_hybrid_llm(monkeypatch):
    def fake_chat(prompt, model=None, max_tokens=1024):
        return {"message": '{"supported": true, "support_ratio": 0.5, "missing_citations": [], "explanation": "ok"}'}

    monkeypatch.setattr("gavellm.tasks.groundedness.chat_completion", fake_chat)
    task = GroundednessTask(JudgeMode.HYBRID)
    case = Case(id="1", payload={"context_snippets": ["a"], "answer": "a. b"})
    j = task.judge(case)
    assert j.pass_fail is True


def test_format_rules_only():
    task = FormatComplianceTask(JudgeMode.RULES_ONLY)
    case = Case(id="1", payload={"instruction": "", "constraints": {"banned_phrases": ["bad"]}, "candidate": "good"})
    j = task.judge(case)
    assert j.pass_fail is True
