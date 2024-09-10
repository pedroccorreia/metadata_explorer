import streamlit as st
from streamlit_extras.grid import grid
from streamlit_extras.tags import tagger_component


import constants
from services.metadata_service import MetadataService
import utils

st.set_page_config(
    page_title="Audio",
    page_icon="🎧",
    layout="wide",    
)

metadata_service = MetadataService(collection_name = constants.AUDIO_FIRESTORE_DATABASE)

def build_list_page(): 
    items = metadata_service.list_all_documents()
    st.write("This page allows you to explore the metadata of the audio files.")
    st.header("List:")

    content_grid = grid(2, vertical_align="center")
    for item in items:
        with content_grid.container(border=True):
            st.subheader(item['name'])
            st.write(f"*Show*: {item['metadata']['show_name']}")
            st.write(f"*Short*: {item['metadata']['short_summary']}")
            with st.expander(label = 'Long Summary', expanded=False):
                st.write(f"{item['metadata']['long_summary']}")
            st.subheader("Labels")
            tagger_component("", utils.get_labels(item['metadata']['subject_topics']))
            with st.expander(label = 'Transcript', expanded=False):
              gcs_uri = f"gs://{constants.OUTPUT_BUCKET}/audio/transcripts/{item['name']}.json"
              json = utils.load_json_from_gcs_uri(gcs_uri)
              st.write(utils.get_transcription_detail(json))
          

st.title("Audio")

build_list_page()