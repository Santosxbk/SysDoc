from sysdoc.utils.system import get_cpu_info, get_disk_info, get_memory_info, get_os_name


def test_system_helpers_return_expected_shapes() -> None:
    os_name = get_os_name()
    cpu = get_cpu_info()
    memory = get_memory_info()
    disk = get_disk_info()

    assert isinstance(os_name, str)
    assert os_name
    assert isinstance(cpu["cores"], int)
    assert cpu["cores"] >= 1
    assert isinstance(memory["total_gb"], float)
    assert memory["total_gb"] >= 0
    assert isinstance(disk["total_gb"], float)
    assert disk["total_gb"] >= 0
