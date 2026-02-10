import logging
from pathlib import Path

logger = logging.getLogger(__name__)

REPO_NAME = Path(__file__).resolve().parent.parent.parent.name


def get_zx_lidar_cache_dir() -> Path:
    """Get the local zx_lidar_cache."""
    return Path(r"F:\.zx_lidar_cache")


def get_filestore_dir() -> Path:
    """Get the local Filestore."""
    return Path(r"F:\Filestore")


def get_cache_dir(*, log_message: bool = False) -> Path:
    """Get the cache directory where input parquet files should be."""
    path = Path.home() / "temp" / REPO_NAME / "cache"
    if log_message:
        msg = f"Cache directory is {path}"
        logger.info(msg)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_out_dir(*, dir_name: str, subdir_name: str | None = None, subsubdir_name: str | None = None) -> Path:
    """Get the output directory."""
    base_path = Path.home() / "temp" / REPO_NAME / dir_name
    path = base_path / subdir_name if subdir_name else base_path
    path = base_path / subsubdir_name if subsubdir_name else base_path
    msg = f"Output directory is {path}"
    logger.info(msg)
    path.mkdir(parents=True, exist_ok=True)
    return path
