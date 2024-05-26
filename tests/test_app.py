"""Test file for app.py"""
import pytest
import requests

API_ENDPOINT="http://localhost:3000"


def test_server_start(start_server):
    """Test the app.py script to ensure server is running."""
    response = requests.get(API_ENDPOINT)
    assert response.status_code == 200
    assert response.text == "Server is running"

def test_validate_endpoint(start_server, get_bad_json_requests, get_good_json_requests):
    """Tests the validate endpoint."""
    # Fail due to wrong structure
    response = requests.post(
        f"{API_ENDPOINT}/validate", 
        json={"req_data": [get_bad_json_requests[-1]]}
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid request. Must contain json with data key."

    # Fail due to validation cases and wrong json fields
    for bad_json, message in get_bad_json_requests:
        response = requests.post(
            f"{API_ENDPOINT}/validate", 
            json={"data": [bad_json]}
        )
        assert response.status_code == 400
        assert response.json()["error"] == message
    
    # Pass Cases
    good_json, _ = get_good_json_requests
    response = requests.post(f"{API_ENDPOINT}/validate", json=good_json)
    assert response.status_code == 200


# Test get factors
def test_getfactors_endpoint(start_server, get_bad_json_requests, get_good_json_requests):
    """Test the get_factors endpoint."""
    # Checking to make sure it attempts validation
    bad_json, message = get_bad_json_requests[2]
    response = requests.post(
        f"{API_ENDPOINT}/get_factors", 
        json={"data": [bad_json]}
    )
    assert response.status_code == 400
    assert response.json()["error"] == message
    
    # Pass Cases
    good_json, correct_results = get_good_json_requests
    response = requests.post(
        f"{API_ENDPOINT}/get_factors", 
        json=good_json
    )
    assert response.status_code == 200
    assert response.json()["results"] == correct_results
