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

if ui_constants.SERVICE_STORAGE not in st.session_state:
    with st.spinner('Getting your experience ready...'):
        # Services initialization
        st.session_state[ui_constants.SERVICE_STORAGE] = StorageService([constants.INPUT_BUCKET, constants.OUTPUT_BUCKET], constants.SERVICE_ACCOUNT_KEY_FILE)



metadata_service = MetadataService(collection_name = constants.IMAGE_FIRESTORE_DATABASE)
storage_service = st.session_state[ui_constants.SERVICE_STORAGE]

#Event handler
def handle_button_click():
    pass


#Page builder

def build_list_page(): 
    items = metadata_service.list_all_documents()
    st.write("This page allows you to explore the metadata of your images.")
    
    with st.spinner('Loading your images...'):
        content_grid = grid(2, vertical_align="center")
        index = 0
        for item in items:
            if 'metadata' in item:
                with content_grid.container(border=True):
                    img_url = storage_service.get_signed_url(item['file_name'])
                    
                    # st.subheader(item['name'])
                    st.markdown(utils.build_item_header(index, item['name']), unsafe_allow_html=True)
                    st.write(f"""*Description:* {item['metadata']['description']}""")
                    st.write(f"""*Photo Type* {item['metadata']['photo_type']}""")
                    st.write(f"""*Location* {item['metadata']['location']}""")
                    st.image(img_url)
                    tagger_component("*Labels*", utils.get_labels(item['metadata']['subject_topics']))
                    
                    entries = []
                    for person in item['metadata']['persons']:
                        entries.append(person['person'])
                    tagger_component("*People*", entries)
                    index +=1
                    
        st.toast('All images loaded', icon='👍')
                    
            
my_logo = utils.add_logo()

header_row = st.columns([6,1], vertical_alignment="center")
header_row[0].title("Images")
header_row[1].image(my_logo)                    

build_list_page()
