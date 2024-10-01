import streamlit as st


class PageMIMICIIIPatientData:
    """A class to manage the display of MIMIC-III Patient Data in Streamlit."""

    def __init__(self, get_dataset, gcs_dataset_path, storage_bucket) -> None:
        """
        Initializes the PageMIMICIIIPatientData with the dataset function.

        :param get_dataset: A callable that retrieves the dataset.
        """
        self.dfs = {}
        self.logged_in = False
        self.get_dataset = get_dataset
        self.gcs_dataset_path = gcs_dataset_path
        self.storage_bucket = storage_bucket

    def login_required(display_func):
        def wrapper(self, *args, **kwargs):
            if self.logged_in:  # Assumes there's a 'logged_in' attribute in the class
                return display_func(self, *args, **kwargs)
            else:
                return self.display_not_logged_in()

        return wrapper

    @login_required
    def display_page(self):
        """Display the MIMIC-III data if the user is logged in."""
        st.write("MIMIC-III Patient Data")
        if not self.dfs:
            returned_dict = self.get_dataset(self.gcs_dataset_path, self.storage_bucket)
            if "error" in returned_dict:
                st.error(returned_dict["error"])
            else:
                self.dfs = returned_dict

            st.write(len(self.dfs))

    def display_not_logged_in(self) -> None:
        """Display the login prompt for PageMIMICIIIPatientData if the user is not logged in."""
        st.write("Please login to view this project's data")

    def set_login_status(self, status) -> None:
        self.logged_in = status
