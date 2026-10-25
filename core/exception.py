"""Project-specific exception types."""

from __future__ import annotations

import sys
from types import TracebackType

__all__ = ["CustomException", "from_current_exception"]


class CustomException(Exception):
    """Exception enriched with the source location of its original failure.

    Pass ``sys`` (or another module exposing ``exc_info``) while handling an
    exception to capture its traceback location and preserve the original
    exception as the cause.
    """

    def __init__(
        self,
        message: str,
        error_detail: object | None = None,
    ) -> None:
        self.message = message
        self.file_name: str | None = None
        self.line_number: int | None = None
        self.original_exception: BaseException | None = None

        exc_info = getattr(error_detail, "exc_info", None)
        if callable(exc_info):
            _, original_exception, traceback = exc_info()
            self.original_exception = original_exception
            self._set_location(traceback)

        super().__init__(self._format_message())

    def _set_location(self, traceback: TracebackType | None) -> None:
        if traceback is None:
            return

        current_traceback = traceback
        while current_traceback.tb_next is not None:
            current_traceback = current_traceback.tb_next
        self.file_name = current_traceback.tb_frame.f_code.co_filename
        self.line_number = current_traceback.tb_lineno

    def _format_message(self) -> str:
        location = ""
        if self.file_name is not None and self.line_number is not None:
            location = f" ({self.file_name}:{self.line_number})"
        return f"{self.message}{location}"

    def __str__(self) -> str:
        return self._format_message()


def from_current_exception(message: str) -> CustomException:
    """Build a project exception from the currently handled exception."""

    return CustomException(message, sys)