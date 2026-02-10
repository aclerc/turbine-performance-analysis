"""Quick script to load and describe a bit of ZX LiDAR data."""
import io
import logging
from pathlib import Path

import pandas as pd

from lidar_analysis.lidar_analysis_funcs import get_zx_lidar_data
from lidar_analysis.settings import get_out_dir
from scripts.logger import setup_logger

logger = logging.getLogger(__name__)
if __name__ == "__main__":
    out_dir = get_out_dir(dir_name=Path(__file__).stem)
    log_fpath = out_dir / f"{Path(__file__).stem}.log"
    setup_logger(log_fpath)
    msg=f"log file path is {log_fpath}"
    logger.info(msg)

    zx_device_id = 2429 #2429 is Altahullion 2 ground mounted LiDAR
    df = get_zx_lidar_data(
        zx_device_id=zx_device_id,
        start_dt=pd.Timestamp("2025-12-20"),
        end_dt_excl=pd.Timestamp("2026-01-20"),
        cache_dir=None,
    )
    msg = f"{df.head()=}"
    logger.info(msg)
    msg = f"{df.tail()=}"
    logger.info(msg)
    msg = f"{df.describe()=}"
    logger.info(msg)
    buffer = io.StringIO()
    df.info(buf=buffer)
    msg=f"DataFrame info:\n{buffer.getvalue()}"
    logger.info(msg)
