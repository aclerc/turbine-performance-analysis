import datetime as dt
import logging
import math
from pathlib import Path
from typing import TypeVar

import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype

from .settings import get_zx_lidar_cache_dir

logger = logging.getLogger(__name__)

LIDAR_AIR_DENSITY_COL = "Air Density (kg/m3)"
WTG_AIR_DENSITY_COL = "air_density"
WTG_LIDAR_HH_WS_COL = "calibrated lidar HH ws"
WTG_LIDAR_YE_COL = "lidar measured yaw error"

NumericType = TypeVar("NumericType", pd.Series, np.ndarray, float)


def calc_cp(
    *,
    power_kw: NumericType,
    ws_ms: NumericType,
    air_density_kgpm3: NumericType,
    rotor_diameter_m: float,
) -> NumericType:
    """Calculate the power coefficient."""
    rotor_area_m2 = math.pi * (rotor_diameter_m / 2) ** 2
    return 1000.0 * power_kw / (0.5 * air_density_kgpm3 * rotor_area_m2 * ws_ms**3)


def calc_air_density(*, temp_c: NumericType, pressure_mbar: NumericType, humidity_percent: NumericType) -> NumericType:
    """Calculate air density using relevant equations from Wikipedia.

    Parameters
    ----------
    temp_c : NumericType
        Air temperature in degrees Celsius
    pressure_mbar : NumericType
        Atmospheric pressure in millibars (mbar) or hectopascals (hPa)
    humidity_percent : NumericType
        Relative humidity as a percentage (0-100)

    Returns
    -------
    NumericType
        Air density in kg/m³

    """
    # Calculate saturation vapor pressure using August-Roche-Magnus formula
    # https://en.wikipedia.org/wiki/Clausius%E2%80%93Clapeyron_relation#Meteorology_and_climatology
    svp_hpa = 6.1094 * np.exp(17.625 * temp_c / (temp_c + 243.04))

    # Calculate actual vapor pressure using relative humidity
    vapor_pressure_hpa = (humidity_percent / 100) * svp_hpa

    # Specific gas constant for dry air (J/(kg·K))
    r_d = 287.058

    # Specific gas constant for water vapor (J/(kg·K))
    r_v = 461.495

    # Convert temperature to Kelvin
    temp_k = temp_c + 273.15

    # Calculate air density using the equation that accounts for humidity
    # https://en.wikipedia.org/wiki/Density_of_air#Humid_air
    # note 1 mbar = 1 hPa, 1mbar = 100 Pa
    return 100 * (pressure_mbar - vapor_pressure_hpa) / (r_d * temp_k) + 100 * vapor_pressure_hpa / (r_v * temp_k)


def calc_air_density_iec(
    *, temp_c: NumericType, pressure_mbar: NumericType, humidity_percent: NumericType
) -> NumericType:
    """Calculate air density as per IEC 61400-12-1.

    Parameters
    ----------
    temp_c : NumericType
        Air temperature in degrees Celsius
    pressure_mbar : NumericType
        Atmospheric pressure in millibars (mbar) or hectopascals (hPa)
    humidity_percent : NumericType
        Relative humidity as a percentage (0-100)

    Returns
    -------
    NumericType
        Air density in kg/m³

    """
    temp_k = temp_c + 273.15
    pressure_pa = pressure_mbar * 100
    r0 = 287.05  # gas constant of dry air
    rw = 461.5  # gas constant of water vapour
    vapour_pressure_pa = 0.0000205 * np.exp(0.0631846 * temp_k)
    return (1 / temp_k) * (pressure_pa / r0 - (humidity_percent / 100) * vapour_pressure_pa * (1 / r0 - 1 / rw))


def _generate_dates_in_range(start_dt: dt.datetime, end_dt_excl: dt.datetime) -> list[dt.date]:
    """Generate dates in a datetime range."""
    date_range = pd.date_range(
        start=start_dt.date(), end=(end_dt_excl - dt.timedelta(microseconds=1)).date(), freq="D", inclusive="both"
    )
    return [date.date() for date in date_range]


def get_zx_lidar_data(
    *,
    start_dt: pd.Timestamp,
    end_dt_excl: pd.Timestamp,
    zx_device_id: int,
    cache_dir: Path | None = None,
) -> pd.DataFrame:
    """Return ZX LiDAR dataframe for any wind farm."""
    cache_fname = (
        f"get_zx_lidar_data_{zx_device_id}_{start_dt.strftime('%Y%m%d%H%M%S')}_"
        f"{end_dt_excl.strftime('%Y%m%d%H%M%S')}.parquet"
    )
    if cache_dir is not None and (cache_dir / cache_fname).exists():
        return pd.read_parquet(cache_dir / cache_fname)
    device_decr = "ZTM" if zx_device_id >= 5000 else ""  # noqa:PLR2004
    file_paths = [
        get_zx_lidar_cache_dir()
        / "timeseries"
        / str(zx_device_id)
        / f"Wind_{device_decr}{zx_device_id}@{d.strftime('Y%Y_M%m_D%d')}.parquet"
        for d in _generate_dates_in_range(start_dt=start_dt, end_dt_excl=end_dt_excl)
    ]
    dfs = []
    for file_path in file_paths:
        try:
            _df = pd.read_parquet(file_path)
        except FileNotFoundError:
            msg = f"File {file_path} not found."
            logger.warning(msg)
            continue
        _df = _df.drop(columns=[x for x in _df.columns if x.startswith("Checksum")])
        # find a good timestamp column
        if "Timestamp (ISO 8601)" in _df.columns:
            _df["timestamp"] = pd.to_datetime(_df["Timestamp (ISO 8601)"])
            _df["Timestamp (ISO 8601)"] = _df["Timestamp (ISO 8601)"].astype(
                str
            )  # ensure this guys is a string to avoid mixed types
        elif "Time and Date" in _df.columns:
            _df["timestamp"] = pd.to_datetime(_df["Time and Date"], format="%m/%d/%Y %I:%M:%S %p")
            _df["Time and Date"] = _df["Time and Date"].astype(str)  # ensure this guys is a string to avoid mixed types
        if not is_datetime64_any_dtype(_df["timestamp"]):
            msg = f"{_df["timestamp"].dtype=}"
            raise ValueError(msg)
        expected_date = pd.to_datetime(str(file_path).split("@")[-1].split(".")[0], format="Y%Y_M%m_D%d")
        if not (_df["timestamp"] - expected_date).dt.total_seconds().abs().max() < (24 * 3600):
            msg = (
                f"something is wrong:"
                f"\n{file_path=}\n{expected_date=}\n{_df["timestamp"].min()=}\n{_df["timestamp"].max()=}"
            )
            raise ValueError(msg)
        dfs.append(_df)
    return_df = pd.concat(dfs).set_index("timestamp", drop=True) if dfs else pd.DataFrame()
    if return_df.empty:
        return return_df
    return_df = return_df[~return_df.index.duplicated(keep="last")].sort_index()
    # replace bad values with NaN
    for zx_bad_value in [9999, 9991]:
        return_df = return_df.replace(zx_bad_value, np.nan)
    # replace bad Met Pressure values with NaN
    bad_pressure = (return_df["Met Pressure (mbar)"] < 700) | (return_df["Met Pressure (mbar)"] > 1200)  # noqa:PLR2004
    return_df.loc[bad_pressure, "Met Pressure (mbar)"] = np.nan
    # add air density
    return_df[LIDAR_AIR_DENSITY_COL] = calc_air_density_iec(
        temp_c=return_df["Met Air Temp. (C)"],
        pressure_mbar=return_df["Met Pressure (mbar)"],
        humidity_percent=return_df["Met Humidity (%)"],
    )
    bad_air_desnity = (return_df[LIDAR_AIR_DENSITY_COL] < 0.9) | (return_df[LIDAR_AIR_DENSITY_COL] > 1.4)  # noqa:PLR2004
    return_df.loc[bad_air_desnity, LIDAR_AIR_DENSITY_COL] = np.nan
    return_df = (
        return_df[(return_df.index >= pd.Timestamp(start_dt)) & (return_df.index < pd.Timestamp(end_dt_excl))]
    ).sort_index()
    if cache_dir is not None:
        return_df.to_parquet(cache_dir / cache_fname)
        return pd.read_parquet(cache_dir / cache_fname)
    return return_df
