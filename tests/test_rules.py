from gavellm.rules.groundedness import check_groundedness
from gavellm.rules.format import check_format


def test_check_groundedness():
    result = check_groundedness(["Cats purr."], "Cats purr.")
    assert result["supported"]
    assert result["support_ratio"] == 1.0


def test_check_format():
    result = check_format({"banned_phrases": ["bad"]}, "good output")
    assert result["compliant"]
    result = check_format({"banned_phrases": ["bad"]}, "bad output")
    assert not result["compliant"]
