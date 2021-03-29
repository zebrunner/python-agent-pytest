import logging
import os

logging.basicConfig(level=os.getenv("REPORTING_LOG_LEVEL") or "INFO")

__version__ = "0.1.0"
