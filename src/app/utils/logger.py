import logging
from datetime import datetime
from pathlib import Path


class Logger:
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        try:
            # Create logs directory
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)

            log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"

            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)

            # Avoid duplicate handlers
            if logger.handlers:
                return logger

            formatter = logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
            )

            # File handler (safe)
            try:
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                print(f"⚠️ File logging failed: {e}")

            # Console handler (always works)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            return logger

        except Exception as e:
            # Ultimate fallback logger
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