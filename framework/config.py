"""
framework/config.py

Loads environment-specific config from YAML so tests never hardcode
URLs, timeouts, or credentials. Supports multiple environments
(dev/staging/prod-like) selected via an env var, which is exactly how
real test frameworks avoid "works on my machine" config drift.
"""
import os
import yaml

_CONFIG_CACHE = {}


def load_config(env: str = None) -> dict:
    """
    Loads config/<env>.yaml. Defaults to the ENV environment variable,
    falling back to 'default' if not set. Caches per-env so repeated
    calls (e.g. from every test) don't re-read disk.
    """
    env = env or os.environ.get("TEST_ENV", "default")

    if env in _CONFIG_CACHE:
        return _CONFIG_CACHE[env]

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", f"{env}.yaml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"No config found for env '{env}' at {config_path}. "
            f"Create config/{env}.yaml or set TEST_ENV to an existing one."
        )

    with open(config_path, "r") as f:
        data = yaml.safe_load(f)

    _CONFIG_CACHE[env] = data
    return data


def get(key: str, env: str = None, default=None):
    """Dotted-path lookup, e.g. get('browser.headless')."""
    cfg = load_config(env)
    node = cfg
    for part in key.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node
