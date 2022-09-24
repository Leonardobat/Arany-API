from http import HTTPStatus


class TestAuthController:
    def test_valid_login_request(self, client):
        mock_user = {"username": "test", "password": "some"}
        response = client.post("/auth/login", json=mock_user)
        expected_response = {
            "message": f"user {mock_user['username']} logged in successfully"
        }
        expected_status_code = HTTPStatus.OK

        assert expected_status_code == response.status_code
        assert expected_response == response.get_json()

    def test_invalid_login_request(self, client):
        mock_user = {"password": "some", "user": "test"}
        response = client.post("/auth/login", json=mock_user)
        expected_response = {
            "error": "400 Bad Request: Invalid json body expected a body in format: {'username': '', 'password': ''}"
        }

        expected_status_code = HTTPStatus.BAD_REQUEST

        assert expected_status_code == response.status_code
        assert expected_response == response.get_json()

    def test_valid_register_request(self, client):
        mock_user = {"username": "test", "password": "some"}
        response = client.post("/auth/register", json=mock_user)
        expected_response = {
            "message": f"user {mock_user['username']} registered successfully"
        }
        expected_status_code = HTTPStatus.OK

        assert expected_status_code == response.status_code
        assert expected_response == response.get_json()

    def test_invalid_register_request(self, client):
        mock_user = {"password": "some", "user": "test"}
        response = client.post("/auth/register", json=mock_user)
        expected_response = {
            "error": "400 Bad Request: Invalid json body expected a body in format: {'username': '', 'password': ''}"
        }

        expected_status_code = HTTPStatus.BAD_REQUEST

        assert expected_status_code == response.status_code
        assert expected_response == response.get_json()
