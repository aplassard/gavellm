from gavellm import llm


def test_chat_completion_integration():
    result = llm.chat_completion("Say hello!", model="gpt-4o-mini", max_tokens=5)
    assert isinstance(result["message"], str) and result["message"]
    assert isinstance(result["usage"], dict)
