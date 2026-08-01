"""
framework/driver_factory.py

Centralizes browser/context creation so every test gets identical,
config-driven setup (headless mode, window size, timeouts) instead of
each test file configuring Playwright by hand. Swap the config file
and every test in the suite runs differently - no code changes needed.
"""
from playwright.sync_api import sync_playwright
from framework.config import get
from framework.logger import get_logger

logger = get_logger(__name__)


class DriverFactory:
    def __init__(self):
        self._playwright = None
        self._browser = None
        self._context = None

    def create_page(self):
        self._playwright = sync_playwright().start()

        browser_name = get("browser.name", default="chromium")
        headless = get("browser.headless", default=True)
        width = get("browser.window_width", default=1440)
        height = get("browser.window_height", default=900)

        logger.info(
            "Launching browser=%s headless=%s size=%dx%d",
            browser_name, headless, width, height,
        )

        browser_type = getattr(self._playwright, browser_name)
        self._browser = browser_type.launch(headless=headless)
        self._context = self._browser.new_context(
            viewport={"width": width, "height": height}
        )
        page = self._context.new_page()

        default_timeout_ms = get("timeouts.default_wait_seconds", default=10) * 1000
        page.set_default_timeout(default_timeout_ms)

        return page

    def quit(self):
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
        logger.info("Browser session closed.")
