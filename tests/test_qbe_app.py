"""Test file for qbe_app.py"""
import json

import requests

from qbe_app import create_app

API_ENDPOINT = "http://localhost:3000"


def test_script_end_to_end(start_server):  # pylint: disable=unused-argument
    """Test the qbe_app.py script to ensure server is running."""
    response = requests.get(API_ENDPOINT, timeout=1)
    assert response.status_code == 200
    assert response.text == "Server is running"


def test_init(client):
    """Tests initizliation of app and server state"""
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing
    response = client.get("/")
    assert response.data.decode() == "Server is running"


def test_validate_endpoint(client, get_bad_json_requests, get_good_json_requests):
    """Tests the validate endpoint."""
    # Fail due to wrong structure
    response = client.post("/validate", json={"req_data": [get_bad_json_requests[-1]]})
    assert response.status_code == 400
    assert (
        json.loads(response.data.decode())["error"]
        == "Invalid request. Must contain json with data key."
    )
    # Fail due to validation cases and wrong json fields
    for bad_json, error_message in get_bad_json_requests:
        response = client.post("/validate", json={"data": [bad_json]})
        assert response.status_code == 400
        assert json.loads(response.data.decode())["error"] == error_message

    # Pass Cases
    good_json, _ = get_good_json_requests
    response = client.post("/validate", json=good_json)
    assert response.status_code == 200


def test_getfactors_endpoint(client, get_bad_json_requests, get_good_json_requests):
    """Test the get_factors endpoint."""
    # Checking to make sure it attempts validation
    bad_json, message = get_bad_json_requests[2]
    response = client.post("/get_factors", json={"data": [bad_json]})
    assert response.status_code == 400
    assert json.loads(response.data.decode())["error"] == message

    # Pass Cases
    good_json, correct_results = get_good_json_requests
    response = client.post(f"{API_ENDPOINT}/get_factors", json=good_json)
    assert response.status_code == 200
    assert json.loads(response.data.decode())["results"] == correct_results
