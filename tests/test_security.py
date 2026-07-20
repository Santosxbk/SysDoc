from sysdoc.security.security import analyze_security


def test_security_analysis_returns_summary() -> None:
    result = analyze_security()

    assert isinstance(result["is_root"], bool)
    assert isinstance(result["issues"], list)
    assert isinstance(result["recommendation"], str)
