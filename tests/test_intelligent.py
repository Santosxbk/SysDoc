from sysdoc.diagnostics.intelligent import diagnose_system


def test_intelligent_diagnosis_returns_summary() -> None:
    result = diagnose_system()

    assert isinstance(result["summary"], str)
    assert isinstance(result["issues"], list)
    assert isinstance(result["recommendations"], list)
