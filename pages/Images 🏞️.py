import streamlit as st
from streamlit_extras.grid import grid
from streamlit_extras.tags import tagger_component


import constants
from services.metadata_service import MetadataService
import utils

st.set_page_config(
    page_title="Images",
    page_icon="🏞️",
    layout="wide",    
)


metadata_service = MetadataService(collection_name = constants.IMAGE_FIRESTORE_DATABASE)



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
            image_data = utils.get_bytes_from_gcs(f"{constants.INPUT_BUCKET}/{item['file_name']}")
            
            st.subheader(item['name'])
            st.write(f"""*Description:* {item['metadata']['description']}""")
            st.write(f"""*Photo Type* {item['metadata']['photo_type']}""")
            st.write(f"""*Location* {item['metadata']['location']}""")

            
            st.image(image_data)
            tagger_component("*Labels*", utils.get_labels(item['metadata']['subject_topics']))
            
            entries = []
            for person in item['metadata']['persons']:
                entries.append(person['person'])
            tagger_component("*People*", entries)
            



        
st.title("Images")

build_list_page()
