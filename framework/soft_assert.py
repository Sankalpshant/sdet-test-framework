"""
framework/soft_assert.py

Standard hard asserts stop at the first failure - fine for unit tests,
bad for UI/E2E tests where you want to know ALL the things wrong on a
page in one run instead of fixing-and-rerunning five times. This
collects failures and raises once, with everything that went wrong.
"""
from framework.logger import get_logger

logger = get_logger(__name__)


class SoftAssert:
    def __init__(self):
        self._failures = []

    def check(self, condition: bool, message: str):
        if not condition:
            logger.warning("Soft assertion failed: %s", message)
            self._failures.append(message)
        return condition

    def check_equal(self, actual, expected, label: str = ""):
        condition = actual == expected
        msg = f"{label}: expected {expected!r}, got {actual!r}"
        return self.check(condition, msg)

    def assert_all(self):
        """Call at the end of a test to raise if anything was collected."""
        if self._failures:
            details = "\n  - ".join(self._failures)
            raise AssertionError(
                f"{len(self._failures)} soft assertion(s) failed:\n  - {details}"
            )

    @property
    def has_failures(self) -> bool:
        return len(self._failures) > 0
