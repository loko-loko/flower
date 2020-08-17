import os
import sys

from loguru import logger as log


def logger_initialization(log_path, log_file, write_to_file=False, debug=False):
    log_level = "DEBUG" if debug else "INFO"
    formatter="{time:YYYY/MM/DD HH:mm:ss}  {level:<7} {message}"
    log.remove()
    log.add(
        sys.stderr,
        level=log_level,
        format=formatter
    )
    if write_to_file:
        if not os.path.exists:
            log.error(f"[log] No path found from {log_path}")
            exit(1)
        log_file = os.path.join(log_path, log_file)
        log.add(
            log_file,
            level=log_level,
            format=formatter,
            rotation="5 MB"
        )
