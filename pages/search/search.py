import streamlit as st
import pandas as pd
from streamlit_extras.grid import grid
from streamlit_extras.tags import tagger_component
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.bottom_container import bottom
from streamlit_extras.row import row

from constants import AssetTypes
from pages.common.common_components import CommonComponents
from services.search_service import SearchService
import ui_constants
from ui_constants import SearchStatus, SEARCH_STATUS_KEY
import utils

CommonComponents.init_app()

search_service = SearchService()

if ui_constants.LAUNCHPAD_ITEMS not in st.session_state:
    st.session_state[ui_constants.LAUNCHPAD_ITEMS] = []

if ui_constants.SEARCH_STATUS_KEY not in st.session_state:
    st.session_state[ui_constants.SEARCH_STATUS_KEY] = SearchStatus.INIT

def get_asset_name(row):
    return row['metadata']['name']


def show_article():
    st.write('nothing to see here')

def toggle_launchpad(id):
    print(f"Toggled launchpad {id}")
    launchpad_items = st.session_state[ui_constants.LAUNCHPAD_ITEMS]
    if id in launchpad_items:
        st.toast(f'Removed {id}')
        launchpad_items.remove(id)
    else:
        st.toast(f'Added {id}')
        launchpad_items.append(id)

def check_launchpad(id: str) -> bool:
    return id in  st.session_state[ui_constants.LAUNCHPAD_ITEMS]

def clear_launchpad():
    st.session_state[ui_constants.LAUNCHPAD_ITEMS] = []
    st.toast("Launchpad cleared",icon="📋")

def load_results(query):
    return search_service.search(query=query)            



def build_card_entry(index, id, name, summary, subject_topics):
    card_top_row = st.columns([5,1])
    card_top_row[0].markdown(utils.build_item_header(index, name), unsafe_allow_html=True)
    st.write(summary)
    # tagger_component("*Labels*", utils.get_labels(subject_topics))
    card_bottom_row = st.columns([3,2,2])
    
    if check_launchpad(id=id):
        card_bottom_row[1].button('🗑️ Launchpad',key=f"addr{id}",on_click=toggle_launchpad, args=[id])
    else:
        card_bottom_row[1].button('➕ Launchpad',key=f"addr{id}",on_click=toggle_launchpad, args=[id])
        
    card_bottom_row[2].button('Detail↘️', key=f"detail{id}")


def build_card_entries(results : dict):
    filter_row = row(([4,1,2, 2, 1,1,1,1,1]), vertical_align="center")
    filter_row.write("")
    filter_row.write("Segments:")
    filter_row.toggle(label="fold to videos", key="collapse", value=False)
    filter_row.write("")
    filter_row.write("Include:")
    include_audio = filter_row.toggle(label="Audio", key="audio_switch", value=True)
    include_image =filter_row.toggle(label="Images", key="image_switch", value=True)
    include_video = filter_row.toggle(label="Video", key="video_switch", value=True)
    include_articles= filter_row.toggle(label="Articles", key="articles_switch", value=True)

    content_grid = grid(3, vertical_align="center")
    index = 0
    
    for entry in results:
        
            metadata = entry['metadata']
            if(entry['asset_type'] == AssetTypes.ARTICLE.value and include_articles):
                with content_grid.container(border=True):
                    build_card_entry(index, entry['media_id'], 
                                    f"📰 {metadata['name']}",
                                    metadata['summary']['short_summary'],
                                    metadata['summary']['subject_topics'])
                    index +=1
            elif(entry['asset_type'] == AssetTypes.VIDEO.value and include_video):
                with content_grid.container(border=True):
                    build_card_entry(index, entry['media_id'], 
                                    f"🎬 {metadata['name']}",
                                    metadata['summary']['short_summary'],
                                    metadata['summary']['subject_topics'])
                    index +=1
            elif(entry['asset_type'] == AssetTypes.IMAGE.value and include_image):
                with content_grid.container(border=True):
                    build_card_entry(index, entry['media_id'], 
                                f"🏞️ {metadata['name']}",
                                metadata['metadata']['description'],
                                metadata['metadata']['subject_topics'])
                    index +=1
            elif(entry['asset_type'] == AssetTypes.AUDIO.value and include_audio):
                with content_grid.container(border=True):
                    build_card_entry(index, entry['media_id'], 
                                f"🏞️ {metadata['name']}",
                                metadata['metadata']['short_summary'],
                                metadata['metadata']['subject_topics'])
                    index +=1
            #TODO: finish sgement logic
            # elif(entry['asset_type'] == AssetTypes.SEGMENT.value and include_video):
            #     with content_grid.container(border=True):
            #         build_card_entry(index, entry['media_id'], 
            #                     f"🏞️ {metadata['name']}",
            #                     metadata['reason'],
            #                     metadata['start_time'])
            #                     index +=1
            
    
    with bottom():
        num_of_items = len(st.session_state[ui_constants.LAUNCHPAD_ITEMS] )
        st.divider()
        cols = st.columns([2,5,2,2,2])
        cols[1].write("🎬 - Videos | 🏞️ - Images | 📰 - News Article | 🎙️ - Audio")
        cols[2].write(f"Launchpad counter: {num_of_items} ")
        if num_of_items > 0:
            cols[3].button("Clear",type="secondary", on_click=clear_launchpad)
            lets_go = cols[4].button("Launch 🚀")
            if lets_go:
                st.toast("Let's go",icon="🚀")

def build_search_page():
    with st.spinner("Loading your results"):
        results = st.session_state[ui_constants.SEARCH_RESULTS]
        if len(results) > 0:
            build_card_entries(results['search_results'])
        else:
            st.write('No Results found.')


def search_params_change():
    print( f"New query changed {st.session_state[ui_constants.SEARCH_TERM]}")
    query = st.session_state[ui_constants.SEARCH_TERM]
    results = load_results(query)
    print(f"results from search {len(results)}")
    # store results
    st.session_state[ui_constants.SEARCH_RESULTS] = results
    # update status search
    st.session_state[ui_constants.SEARCH_STATUS_KEY] = SearchStatus.RESULTS
    
    
def build_page():
    st.text_input(label="Search", key=ui_constants.SEARCH_TERM , on_change= search_params_change)
    if st.session_state[SEARCH_STATUS_KEY] == SearchStatus.RESULTS:
        build_search_page()
    else:
        st.write('search through your videos, articles, audio and images.')
    

build_page()