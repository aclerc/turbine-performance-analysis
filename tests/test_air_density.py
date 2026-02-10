import itertools

import pytest

from lidar_analysis.lidar_analysis_funcs import calc_air_density, calc_air_density_iec


def test_calc_air_density() -> None:
    """Test two implementations of air density calculation give similar results."""
    for temp_c, pressure_mbar, humidity_percent in itertools.product(
        [-20, 0, 20, 40],
        [900, 950, 1000, 1050],
        [0, 30, 60, 100],
    ):
        expected = calc_air_density(temp_c=temp_c, pressure_mbar=pressure_mbar, humidity_percent=humidity_percent)
        assert calc_air_density_iec(
            temp_c=temp_c, pressure_mbar=pressure_mbar, humidity_percent=humidity_percent
        ) == pytest.approx(expected, abs=5e-3)
