from unittest.mock import MagicMock, patch
import pytest
from ...instruments import osc

@pytest.fixture
def osc():
    mock_rm = MagicMock()
    mock_resource = MagicMock()
    mock_rm.open_resource.return_value = mock_resource
    return osc.Osc(address = "TCPIP0::169.254.58.10::gpib0,1::INSTR", rm = mock_rm)

class TestData:

    def test_data_width_set(self, osc):
        osc.data.data_width.set(2)
        osc.resource.write.assert_called_once_with("DATa:WIDth 2")

    def test_data_width_get(self, osc):
        osc.data.data_width.get()
        osc.resource.query.assert_called_once_with("DATa:WIDth?")

    def test_data_width_invalid(self, osc):
        with pytest.raises(ValueError):
            osc.data.data_width.set(0)

    def test_source_set_ch1(self, osc):
        osc.data.source.set(1)
        osc.resource.write.assert_called_once_with("DATa:SOURCE CH1")

    def test_source_set_ch4(self, osc):
        osc.data.source.set(4)
        osc.resource.write.assert_called_once_with("DATa:SOURCE CH4")

    def test_source_get(self, osc):
        osc.data.source.get()
        osc.resource.query.assert_called_once_with("DATa:SOURCE?")

    def test_source_invalid(self, osc):
        with pytest.raises(ValueError):
            osc.data.source.set(5)

    def test_encoding_set_ascii(self, osc):
        osc.data.encoding.set("ascii")
        osc.resource.write.assert_called_once_with("DATa:ENCDG ASCI")

    def test_encoding_set_ribinary(self, osc):
        osc.data.encoding.set("ribinary")
        osc.resource.write.assert_called_once_with("DATa:ENCDG RIBINARY")

    def test_encoding_set_sribinary(self, osc):
        osc.data.encoding.set("sribinary")
        osc.resource.write.assert_called_once_with("DATa:ENCDG SRIBINARY")

    def test_encoding_case_insensitive(self, osc):
        osc.data.encoding.set("ASCII")
        osc.resource.write.assert_called_once_with("DATa:ENCDG ASCI")

    def test_encoding_get(self, osc):
        osc.data.encoding.get()
        osc.resource.query.assert_called_once_with("DATa:ENCDG?")

    def test_encoding_invalid(self, osc):
        with pytest.raises(ValueError):
            osc.data.encoding.set("notaformat")

    def test_start_set(self, osc):
        osc.data.start.set(100)
        osc.resource.write.assert_called_once_with("DATa:STARt 100")

    def test_start_get(self, osc):
        osc.data.start.get()
        osc.resource.query.assert_called_once_with("DATa:STARt?")

    def test_start_invalid(self, osc):
        with pytest.raises(ValueError):
            osc.data.start.set(-1)

    def test_stop_set(self, osc):
        osc.data.stop.set(1000)
        osc.resource.write.assert_called_once_with("DATa:STOP 1000")

    def test_stop_get(self, osc):
        osc.data.stop.get()
        osc.resource.query.assert_called_once_with("DATa:STOP?")

    def test_stop_invalid(self, osc):
        with pytest.raises(ValueError):
            osc.data.stop.set(-1)

    def test_get_curve(self, osc):
        osc.data.get_curve()
        osc.resource.query.assert_called_once_with("CURVe?")

    def test_cannot_assign_source(self, osc):
        with pytest.raises(AttributeError):
            osc.data.source = 1

    def test_cannot_assign_data_width(self, osc):
        with pytest.raises(AttributeError):
            osc.data.data_width = 2
    
    def test_cannot_set_getonly(self, osc):
        with pytest.raises(AttributeError):
            osc.data.x_increment.set(1)

class TestHorizontal:

    def test_scale_set(self, osc):
        osc.horizontal.scale.set(1)
        osc.resource.write.assert_called_once_with("HORizontal:SCAle 1")

    def test_scale_get(self, osc):
        osc.horizontal.scale.get()
        osc.resource.query.assert_called_once_with("HORizontal:SCAle?")

    def test_scale_invalid_zero(self, osc):
        with pytest.raises(ValueError):
            osc.horizontal.scale.set(0)

    def test_scale_invalid_negative(self, osc):
        with pytest.raises(ValueError):
            osc.horizontal.scale.set(-1)

    def test_scale_invalid_float(self, osc):
        with pytest.raises(ValueError):
            osc.horizontal.scale.set(1.5)

    def test_scale_invalid_string(self, osc):
        with pytest.raises(ValueError):
            osc.horizontal.scale.set("fast")

    def test_position_set(self, osc):
        osc.horizontal.position.set(10)
        osc.resource.write.assert_called_once_with("HORIZONTAL:POSITION 10")

    def test_position_set_negative(self, osc):
        osc.horizontal.position.set(-10)
        osc.resource.write.assert_called_once_with("HORIZONTAL:POSITION -10")

    def test_position_get(self, osc):
        osc.horizontal.position.get()
        osc.resource.query.assert_called_once_with("HORizontal:POSition?")

    def test_position_invalid_float(self, osc):
        with pytest.raises(Exception):
            osc.horizontal.position.set(1.5)

    def test_position_invalid_string(self, osc):
        with pytest.raises(Exception):
            osc.horizontal.position.set("left")

    def test_settings_get(self, osc):
        osc.horizontal.settings.get()
        osc.resource.query.assert_called_once_with("HORizontal?")

    def test_settings_no_setter(self, osc):
        with pytest.raises(AttributeError):
            osc.horizontal.settings.set(1)

    def test_cannot_assign_scale(self, osc):
        with pytest.raises(AttributeError):
            osc.horizontal.scale = 1

    def test_cannot_assign_position(self, osc):
        with pytest.raises(AttributeError):
            osc.horizontal.position = 10

    def test_cannot_assign_settings(self, osc):
        with pytest.raises(AttributeError):
            osc.horizontal.settings = "something"

class TestAcquire:
    def test_params_get(self, osc):
        osc.acquire.params.get()
        osc.resource.query.assert_called_once_with("ACQuire?")

    def test_mode_set_normal(self, osc):
        osc.acquire.mode.set("normal")
        osc.resource.write.assert_called_once_with("ACQuire:MODE NORMal")

    def test_mode_set_peak(self, osc):
        osc.acquire.mode.set("peak")
        osc.resource.write.assert_called_once_with("ACQuire:MODE PEAK")

    def test_mode_set_average(self, osc):
        osc.acquire.mode.set("average")
        osc.resource.write.assert_called_once_with("ACQuire:MODE AVErage")

    def test_mode_set_envelope(self, osc):
        osc.acquire.mode.set("envelope")
        osc.resource.write.assert_called_once_with("ACQuire:MODE ENVelope")

    def test_mode_set_case_insensitive(self, osc):
        osc.acquire.mode.set("NORMAL")
        osc.resource.write.assert_called_once_with("ACQuire:MODE NORMal")

    def test_mode_set_invalid(self, osc):
        with pytest.raises(Exception):
            osc.acquire.mode.set("invalid")

    def test_number_get(self, osc):
        osc.acquire.number.get()
        osc.resource.query.assert_called_once_with("ACQuire:NUMACq?")

    def test_number_set(self, osc):
        osc.acquire.number.set(10)
        osc.resource.write.assert_called_once_with("ACQuire:NUMACq 10")

    def test_number_env_set(self, osc):
        osc.acquire.number_env.set(10)
        osc.resource.write.assert_called_once_with("ACQuire:NUMACq ENVelope 10")

    def test_state_set_on(self, osc):
        osc.acquire.state.set(1)
        osc.resource.write.assert_called_once_with("ACQuire:STATE ON")

    def test_state_set_off(self, osc):
        osc.acquire.state.set(0)
        osc.resource.write.assert_called_once_with("ACQuire:STATE OFF")

    def test_state_set_invalid(self, osc):
        with pytest.raises(Exception):
            osc.acquire.state.set(2)

    def test_stop_after_set_runstop(self, osc):
        osc.acquire.stop_after.set("runstop")
        osc.resource.write.assert_called_once_with("ACQuire:STOPAfter RUNSTop")

    def test_stop_after_set_sequence(self, osc):
        osc.acquire.stop_after.set("sequence")
        osc.resource.write.assert_called_once_with("ACQuire:STOPAfter SEQUENCE")

    def test_stop_after_set_case_insensitive(self, osc):
        osc.acquire.stop_after.set("RUNSTOP")
        osc.resource.write.assert_called_once_with("ACQuire:STOPAfter RUNSTop")

    def test_stop_after_set_invalid(self, osc):
        with pytest.raises(Exception):
            osc.acquire.stop_after.set("invalid")

    def test_cannot_assign_params(self, osc):
        with pytest.raises(AttributeError):
            osc.acquire.params = "something"

    def test_cannot_assign_mode(self, osc):
        with pytest.raises(AttributeError):
            osc.acquire.mode = "normal"

    def test_cannot_assign_number(self, osc):
        with pytest.raises(AttributeError):
            osc.acquire.number = 10

    def test_cannot_assign_state(self, osc):
        with pytest.raises(AttributeError):
            osc.acquire.state = 1

class TestDisplay:
    def test_clear_menu(self, osc):
        osc.display.clear_menu()
        osc.resource.write.assert_called_once_with("CLEARMenu")