from sysdoc.diagnostics.system import analyze_cpu, analyze_disk, analyze_memory


def test_diagnostics_return_recommendations() -> None:
    cpu = analyze_cpu()
    memory = analyze_memory()
    disk = analyze_disk()

    assert isinstance(cpu["recommendation"], str)
    assert isinstance(memory["recommendation"], str)
    assert isinstance(disk["recommendation"], str)
    assert cpu["severity"] in {"low", "medium", "high", "unknown"}
    assert memory["severity"] in {"low", "medium", "high", "unknown"}
    assert disk["severity"] in {"low", "medium", "high", "unknown"}
