import logging
import logging.handlers
import os
import datetime
import sys
from src.core.config import config

# Get log config
LOG_FILE = config.get("logging.log_file", "logs/watercolorinator.log")
LOG_LEVEL = config.get("logging.log_level", "DEBUG").upper()
LOG_TO_FILE = config.get("logging.log_to_file", True)
MAX_LOG_SIZE_MB = config.get("logging.max_log_size_mb", 1)
BACKUP_LOGS = config.get("logging.backup_logs", 5)

# Check if the log file path is absolute, else convert it
if not os.path.isabs(LOG_FILE):
    LOG_FILE = os.path.join(os.path.dirname(__file__), "../../", LOG_FILE)

# Check logs dir existence
LOG_DIR = os.path.dirname(LOG_FILE)
os.makedirs(LOG_DIR, exist_ok=True)

class RFC5424Logger(logging.Logger):
    """Custom logger following RFC 5424 severity levels."""

    # RFC 5424 Levels (Mapping Python Logging)
    EMERGENCY = 70  # 0 - System is unusable
    ALERT = 60  # 1 - Action must be taken immediately
    CRITICAL = 50  # 2 - Critical conditions
    ERROR = 40  # 3 - Error conditions
    WARNING = 30  # 4 - Warning conditions
    NOTICE = 25  # 5 - Normal but significant condition
    INFO = 20  # 6 - Informational messages
    DEBUG = 10  # 7 - Debug-level messages

    def emergency(self, msg, *args, **kwargs):
        """Log a message with severity EMERGENCY (0 in RFC 5424)."""
        if self.isEnabledFor(self.EMERGENCY):
            self._log(self.EMERGENCY, msg, args, **kwargs)

    def alert(self, msg, *args, **kwargs):
        """Log a message with severity ALERT (1 in RFC 5424)."""
        if self.isEnabledFor(self.ALERT):
            self._log(self.ALERT, msg, args, **kwargs)

    def notice(self, msg, *args, **kwargs):
        """Log a message with severity NOTICE (5 in RFC 5424)."""
        if self.isEnabledFor(self.NOTICE):
            self._log(self.NOTICE, msg, args, **kwargs)


# Register the new logging levels
logging.setLoggerClass(RFC5424Logger)
logging.addLevelName(RFC5424Logger.EMERGENCY, "EMERGENCY")
logging.addLevelName(RFC5424Logger.ALERT, "ALERT")
logging.addLevelName(RFC5424Logger.NOTICE, "NOTICE")


class ColoredFormatter(logging.Formatter):
    """Formatter for CLI logs with colors and RFC 5424 levels."""

    COLORS = {
        "DEBUG": "\033[90m",
        "INFO": "\033[94m",
        "NOTICE": "\033[96m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[1;91m",
        "ALERT": "\033[1;95m",
        "EMERGENCY": "\033[1;41m",
        "RESET": "\033[0m",
    }

    def __init__(self, use_utc: bool = False):
        self.use_utc = use_utc
        super().__init__("%(asctime)s [%(levelname)s] (%(name)s): %(message)s")

    def formatTime(self, record, datefmt=None):
        dt = datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc)
        dt = dt.astimezone() if not self.use_utc else dt
        offset = dt.strftime('%z')
        offset_formatted = f"{offset[:3]}:{offset[3:]}"  # Convert ±HHMM to ±HH:MM
        return dt.strftime('%Y-%m-%dT%H:%M:%S') + offset_formatted

    def format(self, record):
        log_message = super().format(record)
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        return f"{color}{log_message}{self.COLORS['RESET']}"


class StandardFormatter(logging.Formatter):
    """Formatter for file logs without ANSI colors (clean logs)."""

    def __init__(self, use_utc: bool = False):
        self.use_utc = use_utc
        super().__init__("%(asctime)s [%(levelname)s] (%(name)s): %(message)s")

    def formatTime(self, record, datefmt=None):
        dt = datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc)
        dt = dt.astimezone() if not self.use_utc else dt
        offset = dt.strftime('%z')
        offset_formatted = f"{offset[:3]}:{offset[3:]}"  # Convert ±HHMM to ±HH:MM
        return dt.strftime('%Y-%m-%dT%H:%M:%S') + offset_formatted


class Logger:
    """Logger wrapper."""

    @staticmethod
    def get_logger(name: str):
        """
        Create and return a structured logger following RFC 5424.

        :param name: Logger name
        :return: Configured logger instance
        """
        _logger = logging.getLogger(name)
        _logger.setLevel(getattr(RFC5424Logger, LOG_LEVEL, logging.DEBUG))

        if _logger.hasHandlers():
            return _logger

        log_to_file = config.get("logging.log_to_file", True)
        use_utc = config.get("logging.use_utc", False)

        console_formatter = ColoredFormatter(use_utc)
        file_formatter = StandardFormatter(use_utc)

        # Console Handler (CLI logs with colors)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(RFC5424Logger, LOG_LEVEL, logging.DEBUG))
        console_handler.setFormatter(console_formatter)
        _logger.addHandler(console_handler)

        # File Handler (persistent logs, no colors)
        if log_to_file:
            file_handler = logging.handlers.RotatingFileHandler(
                LOG_FILE,
                maxBytes=MAX_LOG_SIZE_MB * 1_000_000,
                backupCount=BACKUP_LOGS,
                encoding="utf-8"
            )
            file_handler.setLevel(getattr(RFC5424Logger, LOG_LEVEL, logging.DEBUG))
            file_handler.setFormatter(file_formatter)
            _logger.addHandler(file_handler)

        return _logger


# Example Usage
if __name__ == "__main__":
    logger = Logger.get_logger("Watercolorinator")

    logger.debug("Debugging details")
    logger.info("Normal info message")
    logger.notice("This is a NOTICE message")
    logger.warning("Something might be wrong")
    logger.error("An error occurred!")
    logger.critical("Critical issue detected")
    logger.alert("This is an ALERT!")
    logger.emergency("EMERGENCY! System down!")
