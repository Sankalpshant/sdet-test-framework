"""
framework/base_page.py

Base class every Page Object inherits from. Wraps common Playwright
actions with logging and consistent error handling, so a selector
change or a flaky click failure shows up clearly in logs instead of
a bare stack trace three layers deep in Playwright internals.
"""
from framework.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, url: str):
        logger.info("Navigating to %s", url)
        self.page.goto(url)

    def click(self, selector: str):
        logger.debug("Clicking: %s", selector)
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str):
        logger.debug("Filling '%s' into: %s", value, selector)
        self.page.locator(selector).fill(value)

    def text_of(self, selector: str) -> str:
        return self.page.locator(selector).text_content()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def wait_for_visible(self, selector: str, timeout_ms: int = 10000):
        self.page.locator(selector).wait_for(state="visible", timeout=timeout_ms)

    def screenshot(self, name: str):
        path = f"screenshots/{name}.png"
        self.page.screenshot(path=path)
        logger.info("Screenshot saved: %s", path)
        return path
