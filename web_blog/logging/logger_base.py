import logging
from pathlib2 import Path
from typing import Union, SupportsInt, Any
from logging.handlers import RotatingFileHandler


class Logging(object):
    """
    Logging class for web blog application
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def create_rotating_log(module_name: str, logging_directory: Union[Path, str],
                            level: SupportsInt = logging.INFO) -> Any:
        """
        Creates and returns a logger instance for a module

        Args:
            module_name: name of the python module
            logging_directory: directory where logs are to be placed
            level: logging level
        Returns:
            A logger instance
        """

        logger = logging.getLogger(name=module_name)
        logger.setLevel(level=level)

        log_file = Path(logging_directory) / '{}.log'.format(module_name)
        handler = RotatingFileHandler(filename=str(log_file), maxBytes=20, backupCount=5)

        logger.addHandler(handler)

        return logger


if __name__ == '__main__':
    lgr = Logging.create_rotating_log(module_name=__name__, logging_directory='/tmp', level=logging.INFO)
    lgr.info('test')
