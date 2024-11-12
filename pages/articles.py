import streamlit as st
import pandas as pd
from streamlit_extras.grid import grid
from streamlit_extras.tags import tagger_component

import constants
from pages.common.common_components import CommonComponents
from services.metadata_service import MetadataService
from services.storage_service import StorageService

import ui_constants
import utils

CommonComponents.init_app()

metadata_service = MetadataService(collection_name = 'article-demo')
storage_service = st.session_state[ui_constants.SERVICE_STORAGE]


@st.dialog("Article Detail", width="large")
def show_article(article):
    st.subheader("Item Name:")
    st.text(f"{article['name']}")
    st.title("Headline")
    st.write(f"{article['headline']['headline']}")
    st.subheader("Content:")
    # content is stored  as bytes, so decoding the string to insure proper format
    content = article['content'].decode('utf-8') 
    st.html(content)
    if st.button("Close"):
        st.rerun()

def get_suggested_images(article):
    try:
        images =[storage_service.get_signed_url(article['image_generation_prompts'][i]['image_path']) for i in range(0,2)]
        return images
    except Exception as e:
        print(f"Error getting thumbnails: {e}")
    return []

def build_list_page():
    items = metadata_service.list_all_documents()
    st.write("This page allows you to explore the metadata of your articles.")
    
    with st.spinner('Loading your articles...'):
        content_grid = grid(2, vertical_align="center")
        index = 0
        for item in items:
            with content_grid.container(border=True):
                card_top_row = st.columns([5,1])
                card_top_row[0].markdown(utils.build_item_header(index, item['name']), unsafe_allow_html=True)
                card_top_row[1].button('Full Article ↘️', key = item,on_click=show_article, args=([item]))

                
                
                st.write("Summary:")
                st.write(f"""{item['summary']['short_summary']}""")
                tagger_component("*Labels*", utils.get_labels(item['summary']['subject_topics']))
                
                with st.expander(label='Generated Images', expanded=False):
                    st.image(get_suggested_images(item), width=350)
                
                with st.expander(label='Other Formats', expanded=False):
                    tab1, tab2, tab3 = st.tabs(["Long", "Stories", "Post"])
                    with tab1:
                        st.write(f"""{item['summary']['long_summary']}""")
                    with tab2:
                        st.write('Processing')
                    with tab3:
                        st.write('Processing')

                with st.expander(label='Sentiment Analysis', expanded=False):
                    df = pd.DataFrame(item['sentiment_analysis'])
                    display_df = df[ ['topic','score','magnitude']]
                    #order by magnitude and score
                    display_df = display_df.sort_values(by=['magnitude', 'score'], ascending=False)
                    st.table(display_df)
                index +=1
    st.toast('All articles loaded',icon='👍')

build_list_page()