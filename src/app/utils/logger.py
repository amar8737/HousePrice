import logging
import os
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

class Logger:
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        try:
            # 1. Create logs directory
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)

            log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"

            # 2. Initialize logger
            logger = logging.getLogger(name)
            
            # Use environment variable for log level, default to DEBUG
            log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()
            logger.setLevel(getattr(logging, log_level, logging.DEBUG))
            
            # Prevent duplicate logs and propagation issues
            logger.propagate = False
            if logger.handlers:
                return logger

            formatter = logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
            )

            # 3. Rotating File Handler (Safe implementation)
            try:
                # Max 5MB per file, keeps 3 backups
                file_handler = RotatingFileHandler(
                    log_file, maxBytes=5*1024*1024, backupCount=3
                )
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                print(f"⚠️ File logging failed: {e}")

            # 4. Console Handler (Always works)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            return logger

        except Exception as e:
            # 5. Ultimate fallback logger if setup crashes
            fallback_logger = logging.getLogger("fallback")
            fallback_logger.setLevel(logging.DEBUG)

            if not fallback_logger.handlers:
                console_handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    "%(asctime)s | %(levelname)s | %(message)s"
                )
                console_handler.setFormatter(formatter)
                fallback_logger.addHandler(console_handler)

            fallback_logger.error(f"Logger initialization failed: {e}")
            return fallback_logger