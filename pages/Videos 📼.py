import streamlit as st
from streamlit_extras.row import row
from streamlit_extras.grid import grid
from streamlit_extras.tags import tagger_component

import constants
from services.metadata_service import MetadataService
import ui_constants
import utils

st.set_page_config(
    page_title="Videos",
    page_icon="📼",
    layout="wide",    
)

metadata_service = MetadataService()

# Service Handlers
def get_media_items():
    items = metadata_service.list_all_documents()
    for item in items: 
        item['name'] = item['file_name'].split('.')[0]
        for index, section in enumerate(item['sections']):
            section['order'] = index

    return items

items = get_media_items()

# Event Handlers
def handle_section_click(section): 
    st.session_state[ui_constants.MEDIA_VIEW_TYPE] = ui_constants.MEDIA_VIEW_ITEM_SEGMENT
    st.session_state[ui_constants.MEDIA_ITEM_SEGMENT_CHOSEN] = section

def handle_button_click(item):
    """Event handler for the button click.

    Args:
        file_name: The file_name associated with the clicked button.
    """
    st.session_state[ui_constants.MEDIA_ITEM_CHOSEN] = item
    st.session_state[ui_constants.MEDIA_VIEW_TYPE] = ui_constants.MEDIA_VIEW_ITEM

def handle_back_button_click():
    if( st.session_state[ui_constants.MEDIA_VIEW_TYPE] == ui_constants.MEDIA_VIEW_ITEM ):
        st.session_state[ui_constants.MEDIA_VIEW_TYPE] = ui_constants.MEDIA_VIEW_LIST
    elif( st.session_state[ui_constants.MEDIA_VIEW_TYPE] == ui_constants.MEDIA_VIEW_ITEM_SEGMENT):
        st.session_state[ui_constants.MEDIA_VIEW_TYPE] = ui_constants.MEDIA_VIEW_ITEM

def handle_next_segment_button_click():
    current_item = st.session_state[ui_constants.MEDIA_ITEM_CHOSEN]
    current_section_number = st.session_state[ui_constants.MEDIA_ITEM_SEGMENT_CHOSEN]['order']
    if( current_section_number < len(current_item['sections']) or current_section_number > 0 ):
        st.session_state[ui_constants.MEDIA_ITEM_SEGMENT_CHOSEN] = current_item['sections'][current_section_number+1]

def handle_previous_segment_button_click():
    current_item = st.session_state[ui_constants.MEDIA_ITEM_CHOSEN]
    current_section_number = st.session_state[ui_constants.MEDIA_ITEM_SEGMENT_CHOSEN]['order']
    if( current_section_number < len(current_item['sections']) or current_section_number > 0 ):
        st.session_state[ui_constants.MEDIA_ITEM_SEGMENT_CHOSEN] = current_item['sections'][current_section_number-1]
     
# Builders
def build_list_page():
    docs = []
    for item in items:
        docs.append({
            'File Name': item['file_name'],
            'Created Date': item['created'],
            'Type': item['type']
            })

    st.write("This page allows you to explore the metadata of your videos.")
    st.header("List:")

    content_grid = grid(1, vertical_align="center")
    for index, item in enumerate(items):
        item_container = content_grid.container(border=True)
        card_top_row = item_container.columns([8,1])
        
        card_top_row[0].subheader(f"{index+1} - {item['name']}")
        card_top_row[1].button('Details ↘️', key = item['file_name']+'b',on_click=handle_button_click, args=([item]))

        thumbnails = utils.get_thumbnails(item)
        item_container.image(thumbnails, width=350)
        
def build_detail_page(item):

    header_row = row( [12,2], vertical_align="center")
    header_row.header(item['name'])
    header_row.button(label='Video List ↖️', on_click=handle_back_button_click)

    row1 = row([2,1], vertical_align="center")
    

    VIDEO_URL = f"https://storage.cloud.google.com/{constants.INPUT_BUCKET}/{item['file_name']}"
    st.video(VIDEO_URL, autoplay=True)
    with st.container():
        st.subheader("Summary")
        st.write(item['summary']['short_summary'])
        with st.expander(label='Long Summary', expanded=False):
            
            st.write(item['summary']['long_summary'])
            
        st.subheader("Labels")
        tagger_component("", utils.get_labels(item['summary']['subject_topics']))

    st.subheader("Key Moments")
    sections_grid = grid(3, vertical_align="center")
    
    for section in item['sections']:
        with sections_grid.container(height=250,border=True):
            
            row1 = row([5,2], vertical_align="center")
            row1.subheader(f"{section['order']+1}")
            row1.button('Details ↘️', key=section['reason'], on_click=handle_section_click, args=([section]))

            st.write(f" *Duration*: {section['start_time']} >> {section['end_time']}")
            st.write(f" *Shot Type*: {section['type']}")
            st.write(f" *Reason*: {section['reason']}")
            
def build_section_detail_page(item,  section):    
    header_row = row( [10,5], vertical_align="center")
    header_row.header(f"{item['name']} >> Moment {section['order']+1}")
    header_navigation = header_row.columns(3)
    header_navigation[0].button(label='Video List ↖️', on_click=handle_back_button_click)
    header_navigation[1].button(label='Previous ⬅️ ', on_click=handle_previous_segment_button_click)
    header_navigation[2].button(label='Next ➡️', on_click=handle_next_segment_button_click)

    # create VTT file
    json_object = utils.load_json_from_gcs_uri(section['split_transcription_uri'])

    try:
        utils.json_to_vtt2(json_object, 'output.vtt')
    except:
        st.error('Error creating subtitles', icon="🚨")
        

    VIDEO_URL = utils.get_public_gcs_url(section['split_video_uri'])
    st.video(VIDEO_URL, subtitles='output.vtt', autoplay=True)

    with st.container():
        st.subheader("Section info")
        st.write(f"*Duration:* {section['start_time']} >> {section['end_time']}")
        st.write(f"*Description:* {section['reason']}")
        st.write(f"*Shot Type:* {section['type']}")
        st.write(f"*Moment:* {section['order']+1}/{ len (st.session_state[ui_constants.MEDIA_ITEM_CHOSEN]['sections']) }")
        
    st.subheader("Additional Info")
    
    with st.expander(label="Detail"):
        st.write('The full metadata object for this key moment:')
        st.json(section)

    with st.expander(label='Transcriptions'):
        st.write("the api result of the transcription:")
        st.json(json_object)


# Page Logic
st.title("Videos")

# Start up navigation and state info
if  ui_constants.MEDIA_VIEW_TYPE not in st.session_state:
    st.session_state[ui_constants.MEDIA_VIEW_TYPE] = ui_constants.MEDIA_VIEW_LIST
    st.session_state[ui_constants.MEDIA_ITEM_CHOSEN] = None

#Overall Page Creation
if st.session_state[ui_constants.MEDIA_VIEW_TYPE] == ui_constants.MEDIA_VIEW_LIST:
    st.empty()
    build_list_page()
elif st.session_state[ui_constants.MEDIA_VIEW_TYPE] == ui_constants.MEDIA_VIEW_ITEM:
    st.empty()
    build_detail_page(st.session_state[ui_constants.MEDIA_ITEM_CHOSEN])
elif st.session_state[ui_constants.MEDIA_VIEW_TYPE] == ui_constants.MEDIA_VIEW_ITEM_SEGMENT:
    st.empty()
    build_section_detail_page(st.session_state[ui_constants.MEDIA_ITEM_CHOSEN], st.session_state[ui_constants.MEDIA_ITEM_SEGMENT_CHOSEN])