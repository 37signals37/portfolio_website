import pytest
from src.app import initialize_streamlit, display_login, display_sidebar, display_site
from unittest.mock import patch
import streamlit as st


def test_initialize_streamlit():
    initialize_streamlit()
    assert "loaded_pages" in st.session_state
    assert "logged_in" in st.session_state
    assert not st.session_state.logged_in  # Should be False initially
    assert "selected_page_or_project" in st.session_state


@patch("streamlit.text_input", return_value="user")
@patch("streamlit.button", return_value=True)
@patch("src.app.authenticate_user", return_value={"role": "admin"})
def test_display_login_success(mock_authenticate, mock_button, mock_text_input):
    with patch.dict("streamlit.session_state", {"logged_in": False}, clear=True):
        display_login("api")
        assert st.session_state["logged_in"] == True
        assert st.session_state["role"] == "admin"


@patch("streamlit.text_input", return_value="")
@patch("streamlit.button", return_value=False)
def test_display_login_failure(mock_button, mock_text_input):
    with patch.dict("streamlit.session_state", {"logged_in": False}, clear=True):
        display_login("api")
        assert not st.session_state["logged_in"]


@patch("src.app.display_login")
def test_display_sidebar(mock_display_login):
    display_sidebar("api")
    # Assertions can be made on expected outcomes like changes in session state or function calls


@patch("src.app.display_login")
@patch("streamlit.selectbox", return_value="Welcome")
def test_display_site(mock_selectbox, mock_display_login):
    with patch.dict("streamlit.session_state", {}, clear=True):
        display_site({"user_auth_api": "api"})
        # Check responses based on selectbox value
