"""日志工具。"""

from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import sys
from typing import Optional


DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def _log_root() -> Path:
    return Path(__file__).resolve().parents[3]


def configure_package_logging(
    logger_name: str = "hello_agents",
    log_file: Optional[str] = None,
    file_level: int = logging.INFO,
    console_level: int = logging.WARNING,
) -> logging.Logger:
    """为 hello_agents 包配置日志。

    - 文件日志记录 INFO 及以上，默认写入 `agent_study/logs/8_Memory_and_Retrieval.log`
    - 终端只显示 WARNING 及以上，避免大量 INFO 刷屏
    """
    logger = logging.getLogger(logger_name)

    if getattr(logger, "_hello_agents_configured", False):
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    target_log_file = Path(log_file) if log_file else _log_root() / "logs" / "8_Memory_and_Retrieval.log"
    target_log_file.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(DEFAULT_FORMAT)

    file_handler = RotatingFileHandler(
        target_log_file,
        maxBytes=2 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger._hello_agents_configured = True
    return logger


def setup_logger(
    name: str = "hello_agents",
    level: str = "INFO",
    format_string: Optional[str] = None,
) -> logging.Logger:
    """兼容旧接口。"""
    logger = configure_package_logging(logger_name=name)
    if format_string:
        formatter = logging.Formatter(format_string)
        for handler in logger.handlers:
            handler.setFormatter(formatter)
    logger.setLevel(getattr(logging, level.upper()))
    return logger


def get_logger(name: str = "hello_agents") -> logging.Logger:
    """获取日志记录器。"""
    return logging.getLogger(name)
