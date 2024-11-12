import streamlit as st

import constants
from services.storage_service import StorageService
import ui_constants

class CommonComponents:

    def __init__(self):
        self.pages = {
        "Home": [st.Page("home.py", title="Intro", default=True), 
                st.Page("pages/architecture.py", title="Architecture")],
        
        "1 | Metadata Generation" :
        [
            
                st.Page("pages/videos.py", title="Videos" ),
                st.Page("pages/images.py", title="Images"),
                st.Page("pages/audio.py", title="Audio"),
                st.Page("pages/articles.py", title="Articles"),
            
        ], 
        "2 | Searching & Content Creation": [
                st.Page("pages/search/search.py", title="🔍 Search"),
                st.Page("pages/search/create.py", title="🪄 Create"),
        ]}

    def get_pages(self):
        return self.pages

    def get_page_by_title(self, search_title):
        for page in self.pages:
            if self.pages[page][0].title == search_title:
                return self.pages[page]
        return None

    @staticmethod
    def init_app():
        if ui_constants.SERVICE_STORAGE not in st.session_state:
            with st.spinner('Getting your experience ready...'):
                # Services initialization
                st.session_state[ui_constants.SERVICE_STORAGE] = StorageService([constants.INPUT_BUCKET, constants.OUTPUT_BUCKET], constants.SERVICE_ACCOUNT_KEY_FILE)
