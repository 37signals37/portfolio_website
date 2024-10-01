import json
from src.logger import logger
from google.cloud import secretmanager, storage
from google.api_core.exceptions import GoogleAPICallError
from google.cloud.exceptions import NotFound


def get_config_variables(secret_path) -> dict:
    """
    Fetches configuration variables from GCP Secret Manager, sets up GCP Storage, and returns a dictionary of configuration items.

    Parameters:
        secret_path (str): The GCP path to the secret containing configuration values.

    Returns:
        dict: A dictionary containing keys such as 'user_auth_api' and 'storage_bucket',
              each representing a configured component necessary for the application.

    Raises:
        google.api_core.exceptions.GoogleAPICallError: If the call to the secret manager fails.
        google.cloud.exceptions.NotFound: If the specified bucket or secret does not exist.
        Exception: For general exceptions, more specific exceptions should be handled appropriately.
    """

    config = {}

    secret_client = secretmanager.SecretManagerServiceClient()

    try:
        # # Access the secret version
        response = secret_client.access_secret_version(request={"name": secret_path})

        # # Get the secret payload as bytes
        secret_payload = response.payload.data.decode("UTF-8")

        # # # Convert the payload (JSON) to a dictionary
        gcp_config = json.loads(secret_payload)
    except GoogleAPICallError as e:
        logger.error(f"Failed to access secret version: {e}")
    except NotFound as e:
        logger.error(f"The requested resource was not found: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    try:
        storage_client = storage.Client()
        storage_bucket_name = gcp_config["storage_bucket_name"]
        config["storage_bucket"] = storage_client.get_bucket(storage_bucket_name)

    except NotFound as e:
        logger.error(f"Storage bucket not found: {e}")
    except Exception as e:
        logger.error(f"An error occurred while accessing storage bucket: {e}")

    config["user_auth_api"] = gcp_config["user_auth_api"]
    config["dataset_paths"] = gcp_config["dataset_paths"]

    return config
