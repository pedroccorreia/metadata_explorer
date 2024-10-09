import streamlit as st

from st_pages import get_nav_from_toml

st.set_page_config(layout="wide")

nav = get_nav_from_toml(".streamlit/pages.toml")
pg = st.navigation(nav)
pg.run()