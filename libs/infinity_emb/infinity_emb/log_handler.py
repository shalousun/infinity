# SPDX-License-Identifier: MIT
# Copyright (c) 2023-now michaelfeil

import logging
import os
import sys
from enum import Enum
from typing import Any

logging.getLogger().handlers.clear()

# 新增环境变量支持
DISABLE_RICH_HANDLER = os.getenv("INFINITY_DISABLE_RICH_HANDLER", "false").lower() in {"true", "1", "yes"}
CUSTOM_LOG_FORMAT = os.getenv("INFINITY_LOG_FORMAT", "%(asctime)s %(name)s %(levelname)s: %(message)s")

handlers: list[Any] = []

# 根据环境变量决定是否使用 Rich Handler
if not DISABLE_RICH_HANDLER:
    try:
        from rich.console import Console
        from rich.logging import RichHandler

        handlers.append(RichHandler(console=Console(stderr=True), show_time=False))
    except ImportError:
        handlers.append(logging.StreamHandler(sys.stderr))
else:
    # 强制使用标准 StreamHandler
    handlers.append(logging.StreamHandler(sys.stderr))

LOG_LEVELS: dict[str, int] = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "trace": 5,
}

# 使用环境变量中的格式，如果未设置则使用默认格式
FORMAT = CUSTOM_LOG_FORMAT
logging.basicConfig(
    level="INFO",
    format=FORMAT,
    handlers=handlers,
)

logger = logging.getLogger("infinity_emb")

class UVICORN_LOG_LEVELS(Enum):
    """Re-exports the uvicorn log levels for type hinting and usage."""

    critical = "critical"
    error = "error"
    warning = "warning"
    info = "info"
    debug = "debug"
    trace = "trace"

    def to_int(self) -> int:
        return LOG_LEVELS[self.name]