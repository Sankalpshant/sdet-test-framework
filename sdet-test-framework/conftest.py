"""
conftest.py

Pytest fixtures + hooks shared across the whole suite.

Key feature: automatic screenshot-on-failure. This is a small thing
that makes a real difference in CI - when a test fails on a headless
runner at 3am, a screenshot saved next to the failure is worth more
than any stack trace.
"""
import os
import pytest
from framework.driver_factory import DriverFactory
from framework.api_client import ApiClient
from framework.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture
def page():
    """Provides a fresh Playwright page per test, torn down automatically."""
    factory = DriverFactory()
    pw_page = factory.create_page()
    yield pw_page
    factory.quit()


@pytest.fixture
def api_client():
    return ApiClient()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook into pytest's reporting to auto-capture a screenshot the moment
    a UI test fails - only if the test used the `page` fixture.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page_fixture = item.funcargs.get("page")
        if page_fixture is not None:
            os.makedirs("screenshots", exist_ok=True)
            safe_name = item.name.replace("/", "_").replace(" ", "_")
            path = f"screenshots/FAILED_{safe_name}.png"
            try:
                page_fixture.screenshot(path=path)
                logger.error("Test failed. Screenshot saved: %s", path)
            except Exception as e:
                logger.warning("Could not capture failure screenshot: %s", e)
