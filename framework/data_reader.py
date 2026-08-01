"""
framework/data_reader.py

Reads test data from CSV/JSON so test logic and test data are
separated - a core data-driven-testing principle. Adding a new test
case becomes "add a row," not "write a new test function."
"""
import csv
import json
import os


def read_json(relative_path: str):
    """relative_path is relative to the test_data/ directory."""
    full_path = _resolve(relative_path)
    with open(full_path, "r") as f:
        return json.load(f)


def read_csv(relative_path: str):
    """Returns a list of dicts, one per row, keyed by header."""
    full_path = _resolve(relative_path)
    with open(full_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def _resolve(relative_path: str) -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, "test_data", relative_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Test data file not found: {full_path}")
    return full_path
