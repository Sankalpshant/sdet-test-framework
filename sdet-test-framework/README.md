# SDET Test Framework

A reusable Python test automation framework — not a single test suite, but the *tooling* underneath one. Built to demonstrate framework design: config management, driver/session handling, retry logic, structured logging, data-driven testing, soft assertions, and an API client — the kind of infrastructure an SDET builds so other engineers can write tests faster and more reliably.

## Why this exists

Most portfolio projects are "here's a folder of tests." This is "here's the tooling I'd want underneath those tests at a real company." The example tests in `/tests` are intentionally thin — almost all the interesting logic lives in `/framework`.

## Architecture

```
framework/
  config.py          # YAML-based, per-environment config (no hardcoded URLs/creds)
  logger.py           # structured logging, console + file, used everywhere instead of print()
  decorators.py        # @retry — for legitimately flaky steps, with logged backoff
  data_reader.py        # CSV/JSON test data loading for data-driven tests
  soft_assert.py        # collects multiple failures per test instead of stopping at the first
  api_client.py         # requests wrapper: retry-aware, logged, config-driven base URL
  driver_factory.py       # Playwright browser/context creation, fully config-driven
  base_page.py          # base Page Object — every page inherits logged, consistent actions

config/
  default.yaml          # environment config (browser, timeouts, credentials, URLs)

test_data/
  login_cases.csv        # example data-driven test input

tests/                    # example tests USING the framework
  pages/login_page.py       # example Page Object built on BasePage
  test_login_data_driven.py   # data-driven UI test (reads from CSV)
  test_inventory_soft_assert.py # demonstrates SoftAssert
  test_api_users.py         # demonstrates ApiClient

unit_tests/
  test_framework_utils.py     # unit tests for the framework's OWN code — 12 tests, no browser needed
```

## Key design decisions

- **Config over hardcoding.** Every URL, timeout, and credential lives in `config/default.yaml`. Swapping environments (`TEST_ENV=staging`) requires zero code changes.
- **The framework is tested itself.** `unit_tests/` covers the retry decorator, soft assertions, config loader, and data reader directly — because tooling other people's tests depend on needs its own coverage, not just "it worked when I ran it once."
- **Screenshot-on-failure is automatic**, via a pytest hook in `conftest.py` — not something each test has to remember to call.
- **Soft assertions** exist because in UI/E2E testing, stopping at the first failed check means fixing and re-running five times instead of seeing everything wrong in one pass.

## Running it

```bash
pip install -r requirements.txt
playwright install --with-deps chromium

# Framework's own unit tests (no browser needed)
pytest unit_tests/ -v

# API tests
pytest tests/test_api_users.py -v

# UI tests (data-driven login + soft-assert inventory checks)
pytest tests/test_login_data_driven.py tests/test_inventory_soft_assert.py -v --html=report.html
```

## CI/CD

`.github/workflows/tests.yml` runs unit tests, API tests, and UI tests as separate parallel jobs on every push, uploading the HTML report and any failure screenshots as build artifacts.

---
Built by [Sankalp Shant](https://github.com/Sankalpshant) to demonstrate test framework design, not just test writing.
