"""
unit_tests/test_framework_utils.py

Unit tests for the framework code itself (not the app under test).
A framework with no tests of its own is a red flag - if you're
building tooling other people's tests depend on, that tooling needs
its own coverage.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from framework.decorators import retry
from framework.soft_assert import SoftAssert
from framework.data_reader import read_csv, read_json
from framework.config import get, load_config


class TestRetryDecorator:
    def test_succeeds_on_first_try_without_retrying(self):
        calls = {"count": 0}

        @retry(max_attempts=3, backoff_seconds=0)
        def always_works():
            calls["count"] += 1
            return "ok"

        assert always_works() == "ok"
        assert calls["count"] == 1

    def test_retries_then_succeeds(self):
        calls = {"count": 0}

        @retry(max_attempts=3, backoff_seconds=0)
        def fails_twice_then_succeeds():
            calls["count"] += 1
            if calls["count"] < 3:
                raise ValueError("simulated flaky failure")
            return "ok"

        assert fails_twice_then_succeeds() == "ok"
        assert calls["count"] == 3

    def test_raises_after_max_attempts_exhausted(self):
        @retry(max_attempts=2, backoff_seconds=0)
        def always_fails():
            raise ValueError("permanent failure")

        with pytest.raises(ValueError):
            always_fails()


class TestSoftAssert:
    def test_no_failures_does_not_raise(self):
        soft = SoftAssert()
        soft.check(True, "should pass")
        soft.check_equal(1, 1, "numbers")
        soft.assert_all()  # should not raise

    def test_collects_multiple_failures_and_raises_once(self):
        soft = SoftAssert()
        soft.check(False, "first failure")
        soft.check(False, "second failure")
        soft.check(True, "this one passes")

        with pytest.raises(AssertionError) as exc_info:
            soft.assert_all()

        assert "first failure" in str(exc_info.value)
        assert "second failure" in str(exc_info.value)
        assert "2 soft assertion" in str(exc_info.value)

    def test_has_failures_property(self):
        soft = SoftAssert()
        assert soft.has_failures is False
        soft.check(False, "oops")
        assert soft.has_failures is True


class TestDataReader:
    def test_read_csv_returns_list_of_dicts(self):
        rows = read_csv("login_cases.csv")
        assert len(rows) == 5
        assert rows[0]["case_name"] == "valid_standard_user"
        assert rows[0]["username"] == "standard_user"

    def test_read_csv_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            read_csv("does_not_exist.csv")


class TestConfig:
    def test_load_default_config(self):
        cfg = load_config("default")
        assert cfg["base_url"] == "https://www.saucedemo.com"

    def test_get_dotted_path(self):
        assert get("browser.headless") is True
        assert get("timeouts.default_wait_seconds") == 10

    def test_get_returns_default_for_missing_key(self):
        assert get("nonexistent.key", default="fallback") == "fallback"

    def test_get_credentials_nested(self):
        assert get("credentials.standard_user.username") == "standard_user"
