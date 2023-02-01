import inspect
import logging
import os

import settings


class BaseClass(object):
    log_level = False

    def __init__(self, **kwargs):
        self.log_level = kwargs.get("log_level", False)

    def log(self, message):
        if getattr(settings, "DEBUG") and self.log_level:
            log_level = str(self.log_level).lower()

            debug_filename = os.path.basename(inspect.stack()[1][1])
            debug_function_name = inspect.stack()[1][3]
            debug_line_number = inspect.stack()[1][2]

            message = f"{debug_filename} - {debug_function_name} ({debug_line_number}):\n{message}"

            if log_level == "debug":
                logging.debug(message)
            if log_level == "info":
                logging.info(message)
            if log_level == "warning":
                logging.warning(message)
            if log_level == "error":
                logging.error(message)
            if log_level == "critical":
                logging.critical(message)
            if log_level == "console":
                print(message)
