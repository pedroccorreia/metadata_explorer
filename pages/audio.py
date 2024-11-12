import streamlit as st
from streamlit_extras.grid import grid
from streamlit_extras.tags import tagger_component

from google.cloud import aiplatform

import constants
from pages.common.common_components import CommonComponents
from services.metadata_service import MetadataService
from services.storage_service import StorageService
import ui_constants
import utils

CommonComponents.init_app()

metadata_service = MetadataService(collection_name = constants.AUDIO_FIRESTORE_DATABASE)
storage_service = st.session_state[ui_constants.SERVICE_STORAGE]

if 'current_language' not in st.session_state:
    st.session_state['current_language'] = 'english'


def handle_language_change(new_language: str):
    st.session_state['current_language'] = new_language
    


def build_audio_card(index, item, transcript_json = None, subtitle_file:str = None):
    
    st.markdown(utils.build_item_header(index, item['name']), unsafe_allow_html=True)
            
    # file_gcs_uri = f"gs://{constants.INPUT_BUCKET}/{item['file_name']}"
    video_url = storage_service.get_signed_url(item['file_name'])

    if transcript_json != None:
        st.video(video_url, subtitles=subtitle_file, autoplay=False)
    else:
        st.video(video_url, autoplay=False)

    st.write(f"*Show*: {item['metadata']['show_name']}")
    st.write(f"*Short*: {item['metadata']['short_summary']}")
    st.write(f"{st.session_state['current_language']}")
    translate(item['metadata']['short_summary'])
    with st.expander(label = 'Long Summary', expanded=False):
        st.write(f"{item['metadata']['long_summary']}")
    st.subheader("Labels")
    tagger_component("", utils.get_labels(item['metadata']['subject_topics']))

    
            
    if transcript_json != None:
        with st.expander(label = 'Transcript', expanded=False):
            st.write(utils.get_transcription_detail(transcript_json))

def translate(text):
  # Create a client
  endpoint = aiplatform.Endpoint(f'projects/{constants.PROJECT_ID}/locations/{constants.LOCATION}/publishers/google/models/cloud-translate-text')
  # Initialize the request
  instances=[{
      "source_language_code": 'en-US',
      "target_language_code": 'pt',
      "contents": [text],
      "model": f"projects/{constants.PROJECT_ID}/locations/{constants.LOCATION}/models/general/translation-llm"
  }]
  # Make the request
  response = endpoint.predict(instances=instances)
  # Handle the response
  print(response)


def build_list_page(): 
    items = metadata_service.list_all_documents()
    st.write("This page allows you to explore the metadata of the audio files.")
    cols = st.columns([9,1])
    # Language selection using selectbox
    selected_language = cols[1].selectbox(
        "Language:", 
        ("english", "portuguese", "cantonese", "arabic"),
        key=st.session_state['current_language'] 
    )
    handle_language_change(selected_language)
    
    # # Create language buttons
    # col1, col2, col3, col4 = st.columns(4)
    # with col1:
    #     st.button("English", on_click=handle_language_change, args=("english",))
    # with col2:
    #     st.button("Portuguese", on_click=handle_language_change, args=("portuguese",))
    # with col3:
    #     st.button("Cantonese", on_click=handle_language_change, args=("cantonese",))
    # with col4:
    #     st.button("Arabic", on_click=handle_language_change, args=("arabic",))
    
    content_grid = grid(2, vertical_align="center")
    for index, item in enumerate(items):
        if 'metadata' in item:
            with content_grid.container(border=True):
                transcript_json = None
                gcs_uri = f"gs://{constants.OUTPUT_BUCKET}/audio/transcripts/{item['name']}.json"
                try:
                    transcript_json = utils.load_json_from_gcs_uri(gcs_uri)
                    subtitle_file = f"output_{item['name']}.vtt"
                    utils.json_to_vtt2(transcript_json, subtitle_file)
                    # With transcription / subtitles
                    build_audio_card(index, item, transcript_json=transcript_json, subtitle_file=subtitle_file)
                except Exception as e:
                    print(f"error handling transcript / subtitles for {item['name']} - {e}")
                    # No transcription / subtitles
                    build_audio_card(index, item)
    st.toast('All audio files loaded', icon='👍')


my_logo = utils.add_logo()

header_row = st.columns([6,1], vertical_alignment="center")
header_row[0].title("Audio")
header_row[1].image(my_logo)                    

build_list_page()