def test_index_request(client):
    response = client.get("/")
    expected_response = {"message": "read the OpenApi to discover the api routes"}
    assert expected_response == response.get_json()
