import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
import os

# Set up logging =====================================================
class APILogger(Logger):
    def __init__(self, name, level = logging.INFO):
        super().__init__(name, level)

        # Ensure the logs directory exists
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Set up log handlers and formatters
        formatter = logging.Formatter(
            '%(levelname)s:%(asctime)s:%(name)s:%(message)s'
        )

        file_handler = TimedRotatingFileHandler(
            os.path.join(log_dir, 'info.log'),
            when='midnight',
            interval=1,
            backupCount=10
        )
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

        # Add a stream handler for console output
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.addHandler(stream_handler)

# Set up logging =====================================================