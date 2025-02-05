"""
OpenLEDEval (ole) utilities
"""

import logging
import re
import sys
from datetime import datetime

BASE_LOGGER_NAME = "ole"

__all__ = ["get_logger", "get_valid_filename"]


class SuspiciousFileOperationError(Exception):
    """Generated when a user does something suspicious with file names"""


def get_valid_filename(name: str) -> str:
    """Clean / validate filename string

    Parameters
    ----------
    name : str
        The string to be cleaned for file name validity

    Returns
    -------
    str
        A clean filename

    Raises
    ------
    SuspiciousFileOperation
        if the cleaned string looks like a spooky filepath (i.e. '/', '.', etc...)
    """
    s = str(name).strip().replace(" ", "_")
    s = re.sub(r"(?u)[^-\w.]", "", s)
    s = re.sub(r"_+-+_+", "__", s)
    if s in {"", ".", ".."}:
        raise SuspiciousFileOperationError(f"Could not derive file name from '{name}'")
    return s


def get_logger(name: str = "") -> logging.Logger:
    """Create a logger for the ole module

    Parameters
    ----------
    name : str, default ""
        Names a sub-logger for level management. Default "" returns base logger
        for ole

    Returns
    -------
    logging.Logger
    """
    if name == "":
        return logging.getLogger(f"{BASE_LOGGER_NAME}")
    return logging.getLogger(f"{BASE_LOGGER_NAME}.{name}")


SYSTEM_TIME_ZONE = tz = datetime.now().astimezone().tzinfo


def datetime_now() -> datetime:
    """Return time zone aware datetime object

    Returns
    -------
    datetime
    """

    return datetime.now(tz=SYSTEM_TIME_ZONE)


BASE_LOGGER = get_logger()
BASE_LOGGER.setLevel("INFO")
BASE_LOGGER.addHandler(logging.StreamHandler(sys.stdout))
