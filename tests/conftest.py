import pytest
import time
from subprocess import Popen
import os
import platform


@pytest.fixture(scope='module')
def start_server():
    """Fixture for starting the server for testing"""
    if platform.system() == "Windows":
        venv_path = os.path.join(os.getcwd(), '.venv', 'Scripts', 'python.exe')
    elif platform.system() == "Linux": # or Darwin for MacOS
        venv_path = os.path.join(os.getcwd(), '.venv', 'bin', 'python')

    process = Popen([venv_path, 'app.py'])
    time.sleep(2)
    yield True
    process.terminate()
    process.wait()

@pytest.fixture
def get_bad_json_requests():
    """Returns bad jsons and their expected error messages."""
    return [
        (
            {"var":"age_group", "category":"USA"},
            "Invalid json. Must contain var_name and category fields."
        ),
        (
            {"var_name":"coutnry", "cat":"USA"},
            "Invalid json. Must contain var_name and category fields."
        ),
        (
            {"var_name":"american", "category":"USA"},
            "Invalid var_name: american."
        ),
        (
            {"var_name":"age_group", "category":"0-12"},
            "Invalid pair of var_name: age_group and category: 0-12."
        ),
        (
            {"var_name":"europe", "category":"Italy"},
            "Invalid var_name: europe."
        ),
        (
            {"var_name":"country", "category":"50+"},
            "Invalid pair of var_name: country and category: 50+."
        )
    ]

@pytest.fixture
def get_good_json_requests():
    """Returns good json requests and their expected error messages."""
    return ({
        "data": [
            {"var_name": "country", "category": "UK"},
            {"var_name": "age_group", "category": "30-50"}
        ]
    },
    [
        {
            "category": "UK",
            "factor": 0.25,
            "var_name": "country"
        },
        {
            "category": "30-50",
            "factor": 0.33,
            "var_name": "age_group"
        }
    ]
    )