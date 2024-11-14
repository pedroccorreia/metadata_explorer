from concurrent.futures import thread
import streamlit as st
from streamlit_extras.row import row
from streamlit_extras.grid import grid
from streamlit_extras.tags import tagger_component

import constants
from pages.common.common_components import CommonComponents
from services.metadata_service import MetadataService
from services.storage_service import StorageService
import ui_constants
import utils

CommonComponents.init_app()

metadata_service = MetadataService()
storage_service = st.session_state[ui_constants.SERVICE_STORAGE]


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
def handle_section_click(section, number_sections): 
    st.session_state[ui_constants.MEDIA_VIEW_TYPE] = ui_constants.MEDIA_VIEW_ITEM_SEGMENT
    st.session_state[ui_constants.MEDIA_ITEM_SEGMENT_CHOSEN] = section
    st.session_state[ui_constants.MEDIA_ITEM_INDEX_CHOSEN] = section['order']
    st.session_state[ui_constants.MEDIA_ITEM_SECTIONS_LENGTH] = number_sections

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
        st.session_state[ui_constants.MEDIA_ITEM_INDEX_CHOSEN] = current_section_number + 1 

def handle_previous_segment_button_click():
    current_item = st.session_state[ui_constants.MEDIA_ITEM_CHOSEN]
    current_section_number = st.session_state[ui_constants.MEDIA_ITEM_SEGMENT_CHOSEN]['order']
    if( current_section_number < len(current_item['sections']) or current_section_number > 0 ):
        st.session_state[ui_constants.MEDIA_ITEM_SEGMENT_CHOSEN] = current_item['sections'][current_section_number-1]
        st.session_state[ui_constants.MEDIA_ITEM_INDEX_CHOSEN] = current_section_number - 1
     
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
    
    with st.spinner('Loading your videos...'):
        content_grid = grid(1, vertical_align="center")
        for index, item in enumerate(items):  
            thumbnails = utils.get_thumbnails(item, storage_service)
            item_container = content_grid.container(border=True)
            card_top_row = item_container.columns([8,1])

            # card_top_row[0].subheader(f"{index+1} - {item['name']}")

            card_top_row[0].markdown(utils.build_item_header(index, item['name']), unsafe_allow_html=True)
            card_top_row[1].button('Details ↘️', key = item['file_name']+'b',on_click=handle_button_click, args=([item]))
            thumbnail_row = item_container.columns(3) 
            thumbnail_row[0].image(thumbnails[0], width=350)
            thumbnail_row[1].image(thumbnails[1], width=350)
            thumbnail_row[2].image(thumbnails[2], width=350)

        st.toast(body='All videos loaded', icon='👍')
            
            
        
def build_detail_page(item):

    header_row = row( [12,2], vertical_align="center")
    header_row.header(item['name'])
    header_row.button(label='Video List ↖️', on_click=handle_back_button_click)

    row1 = row([2,1], vertical_align="center")

    video_uri = storage_service.get_signed_url(item['file_name'])

    st.video(video_uri, autoplay=True)
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
            row1.button('Details ↘️', key=section['reason'], on_click=handle_section_click, args=([section, len(item['sections'])]))

            st.write(f" *Duration*: {section['start_time']} >> {section['end_time']}")
            st.write(f" *Shot Type*: {section['type']}")
            st.write(f" *Reason*: {section['reason']}")
            
def build_section_detail_page(item,  section, index, length):    
    header_row = row( [10,5], vertical_align="center")
    header_row.header(f"{item['name']} >> Moment {section['order']+1}")
    header_navigation = header_row.columns(3)
    header_navigation[0].button(label='Video List ↖️', on_click=handle_back_button_click)
    if index == 0:
        header_navigation[1].button(label='Next ➡️', on_click=handle_next_segment_button_click)
    elif index == length-1:
        header_navigation[1].button(label='Previous ⬅️', on_click=handle_previous_segment_button_click)
    else:
        header_navigation[1].button(label='Previous ⬅️', on_click=handle_previous_segment_button_click)
        header_navigation[2].button(label='Next ➡️', on_click=handle_next_segment_button_click)

    # create VTT file
    json_object = utils.load_json_from_gcs_uri(section['split_transcription_uri'])

    try:
        utils.json_to_vtt2(json_object, 'output.vtt')
    except:
        st.error('Error creating subtitles', icon="🚨")
        
    video_path = '/'.join(section['split_video_uri'].split('/')[3:])
    video_url = storage_service.get_signed_url(video_path)

    st.video(video_url, subtitles='output.vtt', autoplay=True)

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
my_logo = utils.add_logo()

header_row = st.columns([6,1], vertical_alignment="center")
header_row[0].title("Videos")
header_row[1].image(my_logo)                    

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
    if ui_constants.MEDIA_ITEM_INDEX_CHOSEN not in st.session_state:
        st.session_state[ui_constants.MEDIA_ITEM_INDEX_CHOSEN] = 0
    if ui_constants.MEDIA_ITEM_SECTIONS_LENGTH not in st.session_state:
        st.session_state[ui_constants.MEDIA_ITEM_INDEX_CHOSEN] = len(st.session_state[ui_constants.MEDIA_ITEM_CHOSEN]['sections'])
    build_section_detail_page(st.session_state[ui_constants.MEDIA_ITEM_CHOSEN], st.session_state[ui_constants.MEDIA_ITEM_SEGMENT_CHOSEN], st.session_state[ui_constants.MEDIA_ITEM_INDEX_CHOSEN], st.session_state[ui_constants.MEDIA_ITEM_SECTIONS_LENGTH])