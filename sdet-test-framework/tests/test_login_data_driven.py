"""
tests/test_login_data_driven.py

Demonstrates data-driven testing: login scenarios come from
test_data/login_cases.csv, not hardcoded in the test. Adding a new
login scenario to test means adding a CSV row, not writing new code.
"""
import pytest
from framework.data_reader import read_csv
from tests.pages.login_page import LoginPage

login_cases = read_csv("login_cases.csv")


@pytest.mark.parametrize("case", login_cases, ids=[c["case_name"] for c in login_cases])
def test_login_scenarios(page, case):
    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login(case["username"], case["password"])

    if case["expect_success"].lower() == "true":
        assert "inventory.html" in page.url
    else:
        error_text = login_page.get_error_text()
        assert case["expected_error_contains"] in error_text
