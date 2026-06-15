import pyvisa
import pytest
from scpi_simple.instruments import psu as psu
from scpi_simple.subsystems import setpoint as psu_set
from scpi_simple.subsystems import output as outp
import pathlib

INSTRUMENTS_YAML = pathlib.Path(__file__).parent / "instruments.yaml"


@pytest.fixture
def simulated_psu():
    rm = pyvisa.ResourceManager(f"{INSTRUMENTS_YAML}@sim")
    power_supply = psu.Psu(rm, "GPIB::5::INSTR")

    yield power_supply
    power_supply.close()

def test_set_voltage(simulated_psu):
    simulated_psu.set.set_voltage(5.0)
    assert simulated_psu.set.voltage.get() == 5.0

def test_set_current(simulated_psu):
    simulated_psu.set.set_current(2.0)
    assert simulated_psu.set.current.get() == 2.0
    
'''
def test_output_on(simulated_psu):
    simulated_psu.output.set_state(0)
    assert simulated_psu.output.state == "1.0"

def test_output_off(simulated_psu):
    simulated_psu.output.set_state(0)
    assert simulated_psu.output.state == "1.0"
    '''
