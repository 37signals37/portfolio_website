import pandas as pd
from io import StringIO
import os
from requests.exceptions import HTTPError


from logger import logger


def get_dataset(gcs_dataset_path: str, storage_bucket) -> dict:
    """
    Retrieves dataset CSVs from a specified Google Cloud Storage (GCS) bucket and loads them into pandas DataFrames.

    Parameters:
        gcs_dataset_path (str): The path within the GCS bucket where the dataset CSV files are stored.
                                This should not be None and must be a valid GCS path.
        storage_bucket (Bucket): The GCS Bucket object that will be used to access the files. This object must have
                                appropriate permissions set to read from the specified path.

    Returns:
        dict: A dictionary where each key is the filename of a CSV file, and the corresponding value is a DataFrame
            containing the data from that CSV file. If an error occurs, returns a dictionary with a single key 'error'
            and the value as the error message.

    Raises:
        HTTPError: If there is an issue accessing the GCS bucket (e.g., network issues, permissions errors).
        Exception: If any unexpected errors occur during the processing of the files.

    Example:
        # Assuming `bucket` is a valid GCS Bucket object and the CSV files are located in 'path/to/datasets/'
        dataset_dfs = get_dataset('path/to/datasets/', bucket)
        if 'error' in dataset_dfs:
            print("Error fetching datasets:", dataset_dfs['error'])
        else:
            for filename, df in dataset_dfs.items():
                print(f"Data from {filename}:", df.head())

    Notes:
        - The function is designed to stop reading and return the data after processing one CSV file when in
        development mode. Make sure to remove any development shortcuts before deployment.
        - Ensure that the GCS bucket object is authenticated and has the correct permissions set before passing it to
        this function.
    """

    # Get the bucket and the blob (file) from GCS
    blobs = storage_bucket.list_blobs(prefix=gcs_dataset_path)

    # Dictionary to store DataFrames
    dataframes = {}

    try:
        # Loop through each file and load it into a DataFrame
        for blob in blobs:
            if blob.name.endswith(".csv"):

                # # Extract file name (optional, for identifying the dataframe)
                file_name = os.path.basename(blob.name)

                # # Download the file's contents as a string
                content = blob.download_as_text()

                # # Read the CSV file into a DataFrame
                df = pd.read_csv(StringIO(content))

                # # Store the DataFrame in the dictionary using the file name as the key
                dataframes[file_name] = df

                # # Here for memory conserving purposes during development
                break

        return dataframes
    except HTTPError as http_err:
        logger.log_error(
            f"HTTP error occurred when accessing GCS: {http_err.response.status_code} - {http_err.response.reason}"
        )
        return {
            "error": f"HTTP error occurred when accessing GCS: {http_err.response.status_code} - {http_err.response.reason}"
        }
    except Exception as e:
        logger.log_error(
            f"An unexpected error occurred while retrieving the dataset: {str(e)}"
        )
        return {
            "error": f"An unexpected error occurred while retrieving the dataset: {str(e)}"
        }
