"""
framework/api_client.py

Thin wrapper around requests that adds: automatic base_url resolution,
request/response logging (for debugging failed API tests), and retry
on transient network errors. This is the kind of utility a hardcoded
requests.get() in every test file doesn't give you for free.
"""
import requests
from framework.config import get
from framework.decorators import retry
from framework.logger import get_logger

logger = get_logger(__name__)


class ApiClient:
    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = base_url or get("api_base_url")
        self.timeout = timeout or get("timeouts.api_timeout_seconds", default=8)
        # ReqRes now requires this header on every request (added after this
        # framework's initial build - APIs change, and hardcoding around that
        # instead of hardcoding it away is the actual lesson here).
        self.default_headers = {"x-api-key": "reqres-free-v1"}

    def _merged_headers(self, headers: dict = None) -> dict:
        merged = dict(self.default_headers)
        if headers:
            merged.update(headers)
        return merged

    def _url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    @retry(max_attempts=3, backoff_seconds=1, exceptions=(requests.exceptions.RequestException,))
    def get(self, path: str, params: dict = None, headers: dict = None):
        url = self._url(path)
        logger.info("GET %s params=%s", url, params)
        resp = requests.get(url, params=params, headers=self._merged_headers(headers), timeout=self.timeout)
        logger.info("-> %s (%dms)", resp.status_code, int(resp.elapsed.total_seconds() * 1000))
        return resp

    @retry(max_attempts=3, backoff_seconds=1, exceptions=(requests.exceptions.RequestException,))
    def post(self, path: str, json_body: dict = None, headers: dict = None):
        url = self._url(path)
        logger.info("POST %s body=%s", url, json_body)
        resp = requests.post(url, json=json_body, headers=self._merged_headers(headers), timeout=self.timeout)
        logger.info("-> %s (%dms)", resp.status_code, int(resp.elapsed.total_seconds() * 1000))
        return resp

    @retry(max_attempts=3, backoff_seconds=1, exceptions=(requests.exceptions.RequestException,))
    def put(self, path: str, json_body: dict = None, headers: dict = None):
        url = self._url(path)
        logger.info("PUT %s body=%s", url, json_body)
        resp = requests.put(url, json=json_body, headers=self._merged_headers(headers), timeout=self.timeout)
        logger.info("-> %s (%dms)", resp.status_code, int(resp.elapsed.total_seconds() * 1000))
        return resp

    @retry(max_attempts=3, backoff_seconds=1, exceptions=(requests.exceptions.RequestException,))
    def delete(self, path: str, headers: dict = None):
        url = self._url(path)
        logger.info("DELETE %s", url)
        resp = requests.delete(url, headers=self._merged_headers(headers), timeout=self.timeout)
        logger.info("-> %s (%dms)", resp.status_code, int(resp.elapsed.total_seconds() * 1000))
        return resp
