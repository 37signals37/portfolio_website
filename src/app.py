import streamlit as st
import os
from src.logger import logger
from src.page_mimic_iii_patient_data import PageMIMICIIIPatientData
from src.authentication_manager import authenticate_user
from src.dataset_manager import get_dataset
from src.environment_configurator import get_config_variables


def initialize_streamlit() -> None:
    """Sets the page display configuration and initializes most Streamlit session_state variables"""

    st.set_page_config(page_title="Eric Brunner Portfolio", layout="wide")

    if "loaded_pages" not in st.session_state:
        st.session_state.loaded_pages = {}
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
    if "selected_page_or_projects" not in st.session_state:
        st.session_state.selected_page_or_project = None


@st.fragment
def display_login(user_auth_api) -> None:
    """
    Display the login form if the user is not logged in. @st.fragment ensures this function is rerun for displays purposes after clicking the login button
    """

    if not st.session_state.logged_in:

        st.write("Please login to view all projects and functionality")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            json_response = authenticate_user(username, password, user_auth_api)

            if "role" in json_response:
                st.session_state.logged_in = True
                st.session_state.role = json_response["role"]
                st.rerun()
            if "error" in json_response:
                st.error(json_response["error"])

    else:
        st.write("You are logged in")


def display_sidebar(user_auth_api) -> None:
    """Calls Login form and displays project selection"""
    display_login(user_auth_api)
    selected_page_or_project = st.selectbox(
        "Select page or project: ",
        options=[
            "Welcome",
            "Chatbot - Spontaneous Intracranial Hypotension SME",
            "MIMIC-III Patient Data",
        ],
        index=0,
    )
    st.session_state.selected_page_or_project = selected_page_or_project


def display_site(config: dict) -> None:
    with st.sidebar:
        display_sidebar(config["user_auth_api"])

    if st.session_state.selected_page_or_project == "Welcome":
        st.write("Welcome Page")

    if (
        st.session_state.selected_page_or_project
        == "Chatbot - Spontaneous Intracranial Hypotension SME"
    ):
        st.write("Chatbot")

    if st.session_state.selected_page_or_project == "MIMIC-III Patient Data":
        if "MIMIC-III Patient Data" not in st.session_state.loaded_pages:
            st.session_state.loaded_pages["MIMIC-III Patient Data"] = (
                PageMIMICIIIPatientData(
                    get_dataset,
                    config["dataset_paths"]["MIMICIII"],
                    config["storage_bucket"],
                )
            )
        page = st.session_state.loaded_pages["MIMIC-III Patient Data"]
        page.set_login_status(st.session_state.logged_in)
        page.display_page()


def main() -> None:
    """Main funtion to initialize the app, display the sidebar and display different project views"""

    environment = os.getenv("ENVIRONMENT", None)
    secret_path = os.getenv("SECRET_PATH", None)

    logger.initialize_logger_based_on_environment(environment)

    initialize_streamlit()

    config = get_config_variables(secret_path)

    display_site(config)


if __name__ == "__main__":
    main()
