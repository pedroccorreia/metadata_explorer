import streamlit as st

from pages.common.common_components import CommonComponents

st.set_page_config(layout="wide")

common_components = CommonComponents()

pages =  common_components.get_pages()
st.session_state['CommonComponents'] = common_components

pg = st.navigation(pages)
pg.run()
