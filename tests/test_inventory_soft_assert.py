"""
tests/test_inventory_soft_assert.py

Demonstrates SoftAssert: checks multiple things about the inventory
page and reports every failure at once, instead of stopping at the
first broken assertion.
"""
from framework.soft_assert import SoftAssert
from tests.pages.login_page import LoginPage


def test_inventory_page_multiple_checks(page):
    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login("standard_user", "secret_sauce")

    soft = SoftAssert()
    soft.check(page.locator(".inventory_item").count() == 6, "Expected 6 inventory items")
    soft.check(page.locator(".title").is_visible(), "Page title should be visible")
    soft.check(
        page.locator('[data-test="product-sort-container"]').is_visible(),
        "Sort dropdown should be visible",
    )
    soft.assert_all()
