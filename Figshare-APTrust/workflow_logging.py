import sys
import os
import logging
from datetime import datetime


class Tee:
    """
    Write the same output to multiple streams.

    Used to keep the original terminal output while also
    copying the exact same output into a log file.
    """

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)
            stream.flush()

    def flush(self):
        for stream in self.streams:
            stream.flush()

    def isatty(self):
        """
        Some libraries check whether the stream is a terminal.
        Return True if any wrapped stream is a TTY.
        """
        return any(
            hasattr(stream, "isatty") and stream.isatty()
            for stream in self.streams
        )


def _capture_existing_logging_handlers(log_file):
    """
    Existing logging.StreamHandler objects may already be connected
    directly to the original terminal before sys.stdout/sys.stderr
    are redirected.

    Replace their stream with a Tee so their existing formatted output
    is written to both:
        1. the original terminal
        2. the VTDR log file

    This preserves the existing logging format exactly.
    """

    processed_handlers = set()

    loggers = [logging.getLogger()]

    for logger_object in logging.Logger.manager.loggerDict.values():
        if isinstance(logger_object, logging.Logger):
            loggers.append(logger_object)

    for logger in loggers:
        for handler in logger.handlers:

            handler_id = id(handler)

            if handler_id in processed_handlers:
                continue

            processed_handlers.add(handler_id)

            if (
                isinstance(handler, logging.StreamHandler)
                and not isinstance(handler, logging.FileHandler)
            ):
                original_stream = handler.stream

                # Avoid wrapping a stream twice
                if not isinstance(original_stream, Tee):
                    handler.setStream(
                        Tee(original_stream, log_file)
                    )


def start_logging(log_base_name, workflow_name, article_id):
    """
    Create a VTDR_logs folder one directory above the
    Figshare-APTrust project directory.

    Copy terminal output, stderr, and existing Python logging output
    into a dataset-specific .log file while preserving the original
    terminal output format.

    Example:

        VTDR_RepositoryServices/
        |
        |-- VTDR_logs/
        |   |
        |   `-- VTDR_I00758_RipaG_RipaG_v01_20260803.log
        |
        `-- Figshare-APTrust/
            |
            |-- workflow_logging.py
            |-- IngFolder_Download_TransferBagAPTrust.py
            `-- PubFolder_Download.py
    """

    # -------------------------------------------------------------
    # Determine ../VTDR_logs relative to this code directory
    # -------------------------------------------------------------

    script_directory = os.path.dirname(
        os.path.abspath(__file__)
    )

    parent_directory = os.path.dirname(
        script_directory
    )

    log_directory = os.path.join(
        parent_directory,
        "VTDR_logs"
    )

    os.makedirs(
        log_directory,
        exist_ok=True
    )

    # -------------------------------------------------------------
    # Create dataset-specific log filename
    # -------------------------------------------------------------

    log_filename = f"{log_base_name}.log"

    log_path = os.path.join(
        log_directory,
        log_filename
    )

    # Append instead of overwriting previous workflow output
    log_file = open(
        log_path,
        "a",
        buffering=1
    )

    # -------------------------------------------------------------
    # Save original stdout/stderr
    # -------------------------------------------------------------

    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # -------------------------------------------------------------
    # Capture ordinary print() and stderr output
    # -------------------------------------------------------------

    sys.stdout = Tee(
        original_stdout,
        log_file
    )

    sys.stderr = Tee(
        original_stderr,
        log_file
    )

    # -------------------------------------------------------------
    # IMPORTANT:
    # Capture logging handlers that were created BEFORE this function.
    #
    # This is what captures output such as:
    #
    # 11:01:01 - INFO: Download successful!
    # 11:01:01 - INFO: Performing MD5 checksum ...
    # 11:01:01 - INFO: MD5 Checksum passed!!!
    #
    # while preserving their original formatting.
    # -------------------------------------------------------------

    _capture_existing_logging_handlers(
        log_file
    )

    # -------------------------------------------------------------
    # Workflow header
    # -------------------------------------------------------------

    print()
    print("=" * 80)
    print(
        f"{workflow_name} started: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print(f"Article ID: {article_id}")
    print(f"Log file: {log_path}")
    print("=" * 80)

    return (
        log_file,
        original_stdout,
        original_stderr
    )