"""Test fixtures for test_qbe_app.py"""
import os
import platform
import time
from subprocess import Popen

import pytest

from qbe_app import create_app


@pytest.fixture
def app():
    """Fixture to create an app"""
    qbe_app = create_app({"TESTING": True})
    return qbe_app


@pytest.fixture
def client(app):  # pylint: disable=redefined-outer-name
    """Fixture to create client with test features"""
    return app.test_client()


@pytest.fixture(scope="module")
def start_server():
    """Fixture for starting the server for testing"""
    system_platform = platform.system()
    if system_platform == "Windows":
        venv_path = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
    elif system_platform == "Linux":  # or Darwin for MacOS
        venv_path = os.path.join(os.getcwd(), ".venv", "bin", "python")
    else:
        raise RuntimeError(f"Unsupported platform: {system_platform}")

    with Popen([venv_path, "qbe_app.py"]) as process:
        time.sleep(2)
        yield True
        process.terminate()
        process.wait()


@pytest.fixture
def get_bad_json_requests():
    """Returns bad jsons and their expected error messages."""
    return [
        (
            {"var": "age_group", "category": "USA"},
            "Invalid json. Must contain var_name and category fields.",
        ),
        (
            {"var_name": "country", "cat": "USA"},
            "Invalid json. Must contain var_name and category fields.",
        ),
        ({"var_name": "american", "category": "USA"}, "Invalid var_name: american."),
        (
            {"var_name": "age_group", "category": "0-12"},
            "Invalid pair of var_name: age_group and category: 0-12.",
        ),
        ({"var_name": "europe", "category": "Italy"}, "Invalid var_name: europe."),
        (
            {"var_name": "country", "category": "50+"},
            "Invalid pair of var_name: country and category: 50+.",
        ),
    ]


@pytest.fixture
def get_good_json_requests():
    """Returns good json requests and their expected error messages."""
    return (
        {
            "data": [
                {"var_name": "country", "category": "UK"},
                {"var_name": "age_group", "category": "30-50"},
            ]
        },
        [
            {"category": "UK", "factor": 0.25, "var_name": "country"},
            {"category": "30-50", "factor": 0.33, "var_name": "age_group"},
        ],
    )
