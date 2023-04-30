import logging
import time

# Set up logging configuration
logging.basicConfig(
    # Set the logging level to display messages at or above DEBUG level
    level=logging.INFO,
    # Format the log messages to include the timestamp, log level, and message
    format="%(asctime)s - %(levelname)s - %(message)s",
    # Use a custom timestamp format in UTC (ISO 8601 format)
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)

# Get the root logger to be used throughout the application
logger = logging.getLogger()

# Configure the logger to use UTC time for timestamps
# By default, the logger uses local time; this line changes the converter function to gmtime (UTC)
logging.Formatter.converter = time.gmtime
