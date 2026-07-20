from sysdoc.hardware.monitor import get_battery_info, get_gpu_info, get_temperature_info


def test_hardware_helpers_return_expected_shapes() -> None:
    gpu = get_gpu_info()
    battery = get_battery_info()
    temperatures = get_temperature_info()

    assert isinstance(gpu["model"], str)
    assert isinstance(gpu["memory_mb"], int)
    assert isinstance(battery["available"], bool)
    assert isinstance(battery["percent"], int)
    assert isinstance(temperatures["available"], bool)
    assert isinstance(temperatures["readings"], list)
