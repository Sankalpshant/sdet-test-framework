"""
framework/decorators.py

Retry decorator for operations that can be legitimately flaky
(network calls, elements that render async). This is NOT for hiding
real bugs - it's for the class of failure that's an infra/timing
issue, not a product defect. Logs every retry so flakiness is visible
in CI output rather than silently swallowed.
"""
import time
import functools
from framework.logger import get_logger

logger = get_logger(__name__)


def retry(max_attempts: int = 3, backoff_seconds: float = 1.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(
                        "%s failed on attempt %d/%d: %s",
                        func.__name__, attempt, max_attempts, e,
                    )
                    if attempt < max_attempts:
                        time.sleep(backoff_seconds * attempt)  # linear backoff
            logger.error(
                "%s failed after %d attempts, giving up.", func.__name__, max_attempts
            )
            raise last_exception
        return wrapper
    return decorator
