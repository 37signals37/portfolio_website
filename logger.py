import logging
from google.cloud import logging as google_cloud_logging
import os


class Logger:
    def __init__(self):
        self.client = None
        self.environment = None

    def initialize_logger(self):
        """Initialize the appropriate logger based on environment."""

        if self.environment == "local":
            self.init_local_logger()
        elif self.environment == "gcp_deployed":
            self.init_gcp_logger()

    def init_gcp_logger(self):
        """Initialize Google Cloud Logging client for deployment."""
        logging_client = google_cloud_logging.Client()
        logging_client.setup_logging(log_level=logging.ERROR)
        self.client = logging.getLogger()

    def init_local_logger(self):
        """Initialize standard logging for local development."""
        logging.basicConfig(
            level=logging.INFO,
            filename="website.log",
            filemode="a",
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.client = logging.getLogger()

    def log_info(self, message):
        """Log an informational message."""
        if self.client:
            self.client.info(message)

    def log_error(self, message):
        """Log an error message."""
        if self.client:
            self.client.error(message)

    def initialize_logger_based_on_environment(self, environment: str):
        self.environment = environment
        self.initialize_logger()


logger = Logger()
