from framework.base_page import BasePage
from framework.config import get


class LoginPage(BasePage):
    URL = get("base_url")

    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def open_login_page(self):
        self.open(self.URL)

    def login(self, username: str, password: str):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_text(self) -> str:
        return self.text_of(self.ERROR_MESSAGE)
