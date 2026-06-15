# tests/unit/test_simple_psu.py
from unittest.mock import MagicMock, patch
import pytest
from ...instruments import psu

@pytest.fixture
def psu():
    mock_rm = MagicMock()
    mock_resource = MagicMock()
    mock_rm.open_resource.return_value = mock_resource
    return psu.Psu(address = "TCPIP0::169.254.58.10::gpib0,1::INSTR", rm = mock_rm)

class TestInstrument:
    def test_connect(self):
        mock_rm = MagicMock()
        mock_resource = MagicMock()
        mock_rm.open_resource.return_value = mock_resource

        with patch("pyvisa.ResourceManager", return_value=mock_rm):
            psu = psu.Psu.connect("GPIB::5::INSTR")

        mock_rm.open_resource.assert_called_once_with("GPIB::5::INSTR")
    
    def test_close(self, psu):
        psu.close()
        psu.resource.close.assert_called_once()

class TestSetPoint:
    def test_set_voltage_sends_correct_string(self, psu):
        psu.setpoint.voltage.set(5.0)
        psu.resource.write.assert_called_once_with("VOLT 5.0")

    def test_set_current_sends_correct_string(self, psu):
        psu.setpoint.current.set(0.02)
        psu.resource.write.assert_called_once_with("CURR 0.02")

    def test_set_negative_voltage_exception(self, psu):
        with pytest.raises(ValueError):
            psu.setpoint.voltage.set(-5)
    
    def test_set_negative_current_exception(self, psu):
        with pytest.raises(ValueError):
            psu.setpoint.current.set(-5)
    
    def test_get_voltage_returns_correct_value(self, psu):
        psu.resource.query.return_value = "1.8"
        assert psu.setpoint.voltage.get() == 1.8
    
    def test_get_current_returns_correct_value(self, psu):
        psu.resource.query.return_value = "0.02"
        assert psu.setpoint.current.get() == 0.02
    
    def test_cannot_assign_voltage_directly(self, psu):
        with pytest.raises(AttributeError):
            psu.setpoint.voltage = 1

class TestOutput:
    def test_output_on_sends_correct_string(self, psu):
        psu.output.state.set(1)
        psu.resource.write.assert_called_once_with("OUTP ON")

    def test_output_off_sends_correct_string(self, psu):
        psu.output.state.set(0)
        psu.resource.write.assert_called_once_with("OUTP OFF")
    
    def test_output_get_sends_correct_string(self, psu):
        state = psu.output.state.get()
        psu.resource.query.assert_called_once_with("OUTP?")
    
    def test_output_set_invalid_state_exception(self, psu):
        with pytest.raises(ValueError):
            psu.output.state.set(2)

class TestApply:
    def test_set_apply(self, psu):
        psu.apply.set("P25V", 1.8, 0.02)
        psu.resource.write.assert_called_once_with("APPL P25V, 1.8, 0.02")

    def test_negative_set_apply_exception(self, psu):
        with pytest.raises(ValueError):
            psu.apply.set("P25V", -0.5, 0.02)
    
    def test_set_invalid_channel_exception(self, psu):
        with pytest.raises(ValueError):
            psu.apply.set("P30V", 1.8, 0.02)

class TestSystem:
    def test_beep(self, psu):
        psu.system.beep()
        psu.resource.write.assert_called_once_with("SYSTem:BEEPer:IMMEdiate")


    