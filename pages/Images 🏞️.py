import streamlit as st
from streamlit_extras.grid import grid
from streamlit_extras.tags import tagger_component


import constants
from services.metadata_service import MetadataService
from services.storage_service import StorageService
import ui_constants
import utils

st.set_page_config(
    page_title="Images",
    page_icon="🏞️",
    layout="wide",    
)


metadata_service = MetadataService(collection_name = constants.IMAGE_FIRESTORE_DATABASE)
storage_service = st.session_state[ui_constants.SERVICE_STORAGE]

#Event handler
def handle_button_click():
    pass


#Page builder

def build_list_page(): 
    items = metadata_service.list_all_documents()
    docs = []
    
    st.write("This page allows you to explore the metadata of your images.")
    st.header("List:")

    content_grid = grid(2, vertical_align="center")
    for item in items:
        with content_grid.container(border=True):
            img_url = storage_service.get_signed_url(item['file_name'])
            
            st.subheader(item['name'])
            if 'metadata' in item:
                st.write(f"""*Description:* {item['metadata']['description']}""")
                st.write(f"""*Photo Type* {item['metadata']['photo_type']}""")
                st.write(f"""*Location* {item['metadata']['location']}""")
                st.image(img_url)
                tagger_component("*Labels*", utils.get_labels(item['metadata']['subject_topics']))
                
                entries = []
                for person in item['metadata']['persons']:
                    entries.append(person['person'])
                tagger_component("*People*", entries)
            else:
                st.image(img_url)
                st.write(f"No metadata generated for this item")

            
            
            



        
st.title("Images")

build_list_page()
