from __future__ import annotations

import streamlit as st

from src.ui.constants.navigation import (
    NAVIGATION_LABEL,
    NAVIGATION_OPTIONS,
    SIDEBAR_TITLE,
)
from src.ui.enums.navigation_page import (
    NavigationPage,
)


class Sidebar:
    """
    Main navigation sidebar.
    """

    @staticmethod
    def render() -> NavigationPage:
        sidebar = st.sidebar

        sidebar.title(
            SIDEBAR_TITLE,
        )

        return sidebar.radio(
            NAVIGATION_LABEL,
            NAVIGATION_OPTIONS,
        )