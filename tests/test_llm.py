from json import JSONDecodeError

import pytest

from gavellm import llm


def test_ensure_env_missing_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)
    monkeypatch.setattr("dotenv.load_dotenv", lambda: None)
    with pytest.raises(RuntimeError):
        llm._ensure_env()


def test_chat_completion_retries(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)

    class DummyCompletion:
        def __init__(self):
            self.choices = [type("Obj", (), {"message": type("Obj", (), {"content": "hi"})()})]
            self.usage = {"prompt_tokens": 1, "completion_tokens": 2}

    class DummyCompletions:
        def __init__(self):
            self.calls = 0

        def create(self, model, messages, max_tokens):
            self.calls += 1
            if self.calls == 1:
                raise JSONDecodeError("Err", "", 0)
            return DummyCompletion()

    class DummyChat:
        def __init__(self):
            self.completions = DummyCompletions()

    class DummyOpenAI:
        def __init__(self, **kwargs):
            self.chat = DummyChat()

    monkeypatch.setattr(llm, "OpenAI", DummyOpenAI)
    monkeypatch.setattr(llm.time, "sleep", lambda s: None)

    result = llm.chat_completion("hi")
    assert result == {"message": "hi", "usage": {"prompt_tokens": 1, "completion_tokens": 2}}
