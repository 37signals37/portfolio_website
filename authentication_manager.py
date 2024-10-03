import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout


from logger import logger


def authenticate_user(username: str, password: str, user_auth_api: str) -> dict:
    """
    Authenticate a user against a specified GCP authentication API.

    This function sends a POST request to the authentication API with the username and password,
    handling common network-related exceptions and returning a JSON response indicating the authentication status.

    Parameters:
        username (str): The username of the user attempting to authenticate.
        password (str): The password for the user in plain text. Ensure this is sent over a secure connection.
        user_auth_api (str): The URL of the GCP authentication API endpoint.

    Returns:
        dict: A dictionary containing the authentication status. Typical keys include:
            - 'role': The role of the authenticated user if authentication is successful.
            - 'error': A descriptive error message in case of failure.

    Raises:
        Timeout: If the request times out.
        ConnectionError: If there is a network-related error connecting to the API.
        HTTPError: If an HTTP error occurs during the request.
        Exception: Covers any other unexpected exceptions.

    Example:
        >>> authenticate_user("john_doe", "s3cr3t", "https://api.example.com")
        {'role': 'admin'}

    Note:
        This function expects the API to use HTTP status codes to indicate success or failure.
        A successful authentication is indicated by a 200 status code.
    """

    data = {
        "username": username,
        "password": password,
    }

    try:

        # # Sending the POST request
        response = requests.post(user_auth_api, json=data)
        response.raise_for_status()  # This will handle HTTP errors

        json_response = response.json()

        # # If authentication is successful, "role" will be present in the json_response keys. If it isn't, a single key "error" will be returned in the dictionary with the value below
        if "role" in json_response:
            return json_response
        else:
            return {"error": "User login failed."}

    except Timeout:
        logger.log_error(
            "Timeout - Login request timed out. Please ensure your network connection is stable and try again."
        )
        return {
            "error": "Login request timed out. Please ensure your network connection is stable and try again."
        }
    except ConnectionError:
        logger.log_error(
            "ConnectionError - Failed to connect to the authentication server. Please check your network connection and the server status."
        )
        return {
            "error": "Failed to connect to the authentication server. Please check your network connection and the server status."
        }
    except HTTPError as http_err:
        logger.log_error(
            f"HTTPError - HTTP error occurred: {http_err.response.status_code} - {http_err.response.reason}"
        )
        return {
            "error": f"HTTP error occurred: {http_err.response.status_code} - {http_err.response.reason}"
        }
    except Exception as e:
        logger.log_error(f"Error - An unexpected error occurred: {str(e)}")
        return {"error": f"An unexpected error occurred: {str(e)}"}
