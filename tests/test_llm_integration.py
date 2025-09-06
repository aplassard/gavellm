from gavellm import llm


def test_chat_completion_integration():
    result = llm.chat_completion(
        "Say hello!", model="openai/gpt-5-nano", max_tokens=256
    )
    assert isinstance(result["message"], str) and result["message"]
    assert isinstance(result["usage"], dict)
