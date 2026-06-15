from unittest.mock import MagicMock, patch
import pytest
from ...instruments import osc 

@pytest.fixture
def oscilloscope():
    mock_rm = MagicMock()
    mock_resource = MagicMock()
    mock_rm.open_resource.return_value = mock_resource
    return osc.Osc(address = "TCPIP0::169.254.58.10::gpib0,1::INSTR", rm = mock_rm)

class TestData:

    def test_data_width_set(self, oscilloscope):
        oscilloscope.data.data_width.set(2)
        oscilloscope.resource.write.assert_called_once_with("DATa:WIDth 2")

    def test_data_width_get(self, oscilloscope):
        oscilloscope.data.data_width.get()
        oscilloscope.resource.query.assert_called_once_with("DATa:WIDth?")

    def test_data_width_invalid(self, oscilloscope  ):
        with pytest.raises(ValueError):
            oscilloscope.data.data_width.set(0)

    def test_source_set_ch1(self, oscilloscope):
        oscilloscope.data.source.set(1)
        oscilloscope.resource.write.assert_called_once_with("DATa:SOURCE CH1")

    def test_source_set_ch4(self, oscilloscope):
        oscilloscope.data.source.set(4)
        oscilloscope.resource.write.assert_called_once_with("DATa:SOURCE CH4")

    def test_source_get(self, oscilloscope):
        oscilloscope.data.source.get()
        oscilloscope.resource.query.assert_called_once_with("DATa:SOURCE?")

    def test_source_invalid(self, oscilloscope):
        with pytest.raises(ValueError):
            oscilloscope.data.source.set(5)

    def test_encoding_set_ascii(self, oscilloscope):
        oscilloscope.data.encoding.set("ascii")
        oscilloscope.resource.write.assert_called_once_with("DATa:ENCDG ASCI")

    def test_encoding_set_ribinary(self, oscilloscope):
        oscilloscope.data.encoding.set("ribinary")
        oscilloscope.resource.write.assert_called_once_with("DATa:ENCDG RIBINARY")

    def test_encoding_set_sribinary(self, oscilloscope):
        oscilloscope.data.encoding.set("sribinary")
        oscilloscope.resource.write.assert_called_once_with("DATa:ENCDG SRIBINARY")

    def test_encoding_case_insensitive(self, oscilloscope):
        oscilloscope.data.encoding.set("ASCII")
        oscilloscope.resource.write.assert_called_once_with("DATa:ENCDG ASCI")

    def test_encoding_get(self, oscilloscope):
        oscilloscope.data.encoding.get()
        oscilloscope.resource.query.assert_called_once_with("DATa:ENCDG?")

    def test_encoding_invalid(self, oscilloscope    ):
        with pytest.raises(ValueError):
            oscilloscope.data.encoding.set("notaformat")

    def test_start_set(self, oscilloscope):
        oscilloscope.data.start.set(100)
        oscilloscope.resource.write.assert_called_once_with("DATa:STARt 100")

    def test_start_get(self, oscilloscope):
        oscilloscope.data.start.get()
        oscilloscope.resource.query.assert_called_once_with("DATa:STARt?")

    def test_start_invalid(self, oscilloscope   ):
        with pytest.raises(ValueError):
            oscilloscope.data.start.set(-1)

    def test_stop_set(self, oscilloscope):
        oscilloscope.data.stop.set(1000)
        oscilloscope.resource.write.assert_called_once_with("DATa:STOP 1000")

    def test_stop_get(self, oscilloscope):
        oscilloscope.data.stop.get()
        oscilloscope.resource.query.assert_called_once_with("DATa:STOP?")

    def test_stop_invalid(self, oscilloscope):
        with pytest.raises(ValueError):
            oscilloscope.data.stop.set(-1)

    def test_get_curve(self, oscilloscope):
        oscilloscope.data.get_curve()
        oscilloscope.resource.query_binary_values.assert_called_once_with(
            "CURVe?", datatype='h', is_big_endian=True
        )
    def test_cannot_assign_source(self, oscilloscope):
        with pytest.raises(AttributeError):
            oscilloscope.data.source = 1

    def test_cannot_assign_data_width(self, oscilloscope):
        with pytest.raises(AttributeError):
            oscilloscope.data.data_width = 2
    
    def test_cannot_set_getonly(self, oscilloscope):
        with pytest.raises(AttributeError):
            oscilloscope.data.x_increment.set(1)

class TestHorizontal:

    def test_scale_set(self, oscilloscope):
        oscilloscope.horizontal.scale.set(1)
        oscilloscope.resource.write.assert_called_once_with("HORizontal:SCAle 1")

    def test_scale_get(self, oscilloscope):
        oscilloscope.horizontal.scale.get()
        oscilloscope.resource.query.assert_called_once_with("HORizontal:SCAle?")

    def test_scale_invalid_zero(self, oscilloscope):
        with pytest.raises(ValueError):
            oscilloscope.horizontal.scale.set(0)

    def test_scale_invalid_negative(self, oscilloscope):
        with pytest.raises(ValueError):
            oscilloscope.horizontal.scale.set(-1)

    def test_scale_invalid_float(self, oscilloscope):
        with pytest.raises(ValueError):
            oscilloscope.horizontal.scale.set(1.5)

    def test_scale_invalid_string(self, oscilloscope):
        with pytest.raises(ValueError):
            oscilloscope.horizontal.scale.set("fast")

    def test_position_set(self, oscilloscope):
        oscilloscope.horizontal.position.set(10)
        oscilloscope.resource.write.assert_called_once_with("HORIZONTAL:POSITION 10")

    def test_position_set_negative(self, oscilloscope):
        oscilloscope.horizontal.position.set(-10)
        oscilloscope.resource.write.assert_called_once_with("HORIZONTAL:POSITION -10")

    def test_position_get(self, oscilloscope):
        oscilloscope.horizontal.position.get()
        oscilloscope.resource.query.assert_called_once_with("HORizontal:POSition?")

    def test_position_invalid_float(self, oscilloscope):
        with pytest.raises(Exception):
            oscilloscope.horizontal.position.set(1.5)

    def test_position_invalid_string(self, oscilloscope ):
        with pytest.raises(Exception):
            oscilloscope.horizontal.position.set("left")

    def test_settings_get(self, oscilloscope):
        oscilloscope.horizontal.settings.get()
        oscilloscope.resource.query.assert_called_once_with("HORizontal?")

    def test_settings_no_setter(self, oscilloscope):
        with pytest.raises(AttributeError):
            oscilloscope.horizontal.settings.set(1)

    def test_cannot_assign_scale(self, oscilloscope):
        with pytest.raises(AttributeError):
            oscilloscope.horizontal.scale = 1

    def test_cannot_assign_position(self, oscilloscope):
        with pytest.raises(AttributeError):
            oscilloscope.horizontal.position = 10

    def test_cannot_assign_settings(self, oscilloscope):
        with pytest.raises(AttributeError):
            oscilloscope.horizontal.settings = "something"

class TestAcquire:
    def test_params_get(self, oscilloscope):
        oscilloscope.acquire.params.get()
        oscilloscope.resource.query.assert_called_once_with("ACQuire?")

    def test_mode_set_normal(self, oscilloscope):
        oscilloscope.acquire.mode.set("normal")
        oscilloscope.resource.write.assert_called_once_with("ACQuire:MODE NORMal")

    def test_mode_set_peak(self, oscilloscope):
        oscilloscope.acquire.mode.set("peak")
        oscilloscope.resource.write.assert_called_once_with("ACQuire:MODE PEAK")

    def test_mode_set_average(self, oscilloscope):
        oscilloscope.acquire.mode.set("average")
        oscilloscope.resource.write.assert_called_once_with("ACQuire:MODE AVErage")

    def test_mode_set_envelope(self, oscilloscope):
        oscilloscope.acquire.mode.set("envelope")
        oscilloscope.resource.write.assert_called_once_with("ACQuire:MODE ENVelope")

    def test_mode_set_case_insensitive(self, oscilloscope):
        oscilloscope.acquire.mode.set("NORMAL")
        oscilloscope.resource.write.assert_called_once_with("ACQuire:MODE NORMal")

    def test_mode_set_invalid(self, oscilloscope):
        with pytest.raises(Exception):
            oscilloscope.acquire.mode.set("invalid")

    def test_number_get(self, oscilloscope):
        oscilloscope.acquire.number.get()
        oscilloscope.resource.query.assert_called_once_with("ACQuire:NUMACq?")

    def test_number_set(self, oscilloscope):
        oscilloscope.acquire.number.set(10)
        oscilloscope.resource.write.assert_called_once_with("ACQuire:NUMACq 10")

    def test_number_env_set(self, oscilloscope):
        oscilloscope.acquire.number_env.set(10)
        oscilloscope.resource.write.assert_called_once_with("ACQuire:NUMACq ENVelope 10")

    def test_state_set_on(self, oscilloscope):
        oscilloscope.acquire.state.set(1)
        oscilloscope.resource.write.assert_called_once_with("ACQuire:STATE ON")

    def test_state_set_off(self, oscilloscope):
        oscilloscope.acquire.state.set(0)
        oscilloscope.resource.write.assert_called_once_with("ACQuire:STATE OFF")

    def test_state_set_invalid(self, oscilloscope):
        with pytest.raises(Exception):
            oscilloscope.acquire.state.set(2)

    def test_stop_after_set_runstop(self, oscilloscope):
        oscilloscope.acquire.stop_after.set("runstop")
        oscilloscope.resource.write.assert_called_once_with("ACQuire:STOPAfter RUNSTop")

    def test_stop_after_set_sequence(self, oscilloscope):
        oscilloscope.acquire.stop_after.set("sequence")
        oscilloscope.resource.write.assert_called_once_with("ACQuire:STOPAfter SEQUENCE")

    def test_stop_after_set_case_insensitive(self, oscilloscope):
        oscilloscope.acquire.stop_after.set("RUNSTOP")
        oscilloscope.resource.write.assert_called_once_with("ACQuire:STOPAfter RUNSTop")

    def test_stop_after_set_invalid(self, oscilloscope  ):
        with pytest.raises(Exception):
            oscilloscope.acquire.stop_after.set("invalid")

    def test_cannot_assign_params(self, oscilloscope    ):
        with pytest.raises(AttributeError):
            oscilloscope.acquire.params = "something"

    def test_cannot_assign_mode(self, oscilloscope):
        with pytest.raises(AttributeError):
            oscilloscope.acquire.mode = "normal"

    def test_cannot_assign_number(self, oscilloscope):
        with pytest.raises(AttributeError):
            oscilloscope.acquire.number = 10

    def test_cannot_assign_state(self, oscilloscope):
        with pytest.raises(AttributeError):
            oscilloscope.acquire.state = 1

class TestDisplay:
    def test_clear_menu(self, oscilloscope):
        oscilloscope.display.clear_menu()
        oscilloscope.resource.write.assert_called_once_with("CLEARMenu")