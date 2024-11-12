import time
import streamlit as st
# from streamlit_pills import pills

from pages.common.common_components import CommonComponents
from services.audio_service import AudioService
from services.content_assistance_service import ContentAssistanceService

from services.demo_serivce import DemoService
from services.search_service import SearchService

from ui_constants import CREATE_NEWSLETTER_OPTION, CREATE_OPTIONS, CREATE_PODCAST_OPTION, LAUNCHPAD_ITEMS, PERSONA_CHOSEN, PODCAST_CHOSEN, CreateContentStatus, CREATE_CHOSEN_OPTION, CREATE_STATUS_KEY



CommonComponents.init_app()

#init session variables
if CREATE_CHOSEN_OPTION not in st.session_state:
    st.session_state[CREATE_CHOSEN_OPTION] = None

if CREATE_STATUS_KEY not in st.session_state:
    st.session_state[CREATE_STATUS_KEY] = CreateContentStatus.INIT

if LAUNCHPAD_ITEMS not in st.session_state:
    st.session_state[LAUNCHPAD_ITEMS] = []

#init services
search_service = SearchService()
audio_service = AudioService()
content_service = ContentAssistanceService(generation_model='gemini-1.5-flash-002')
demo_service = DemoService()

#loads input items 
input_items_ids = st.session_state[LAUNCHPAD_ITEMS]
input_content = []
for input_item_id in input_items_ids:
      input_content.append(search_service.get_metadata(input_item_id))
#Convert input_content to a string
input_content_str = ' '.join([str(item) for item in input_content])

#event handlers    
def handle_podcast_chosen():
     st.session_state[CREATE_STATUS_KEY] = CreateContentStatus.PODCAST_CREATE

def handle_newsletter_chosen():
     st.session_state[CREATE_STATUS_KEY] = CreateContentStatus.NEWSLETTER_CREATE

def handle_content_type_action():
     # change status according to option chosen
     if st.session_state[CREATE_CHOSEN_OPTION] == CREATE_PODCAST_OPTION:
         st.session_state[CREATE_STATUS_KEY] = CreateContentStatus.PODCAST_OPTIONS
     elif st.session_state[CREATE_CHOSEN_OPTION] == CREATE_NEWSLETTER_OPTION:
         st.session_state[CREATE_STATUS_KEY] = CreateContentStatus.NEWSLETTER_OPTIONS
     

def build_creation_options():
    with st.expander(label="Actions", expanded=True):
            st.write("You can now create content based on these items.")
            #combo box with Generate Podcast, Storyline
            option = st.selectbox(label="Actions",  options=CREATE_OPTIONS, on_change=handle_content_type_action, key=CREATE_CHOSEN_OPTION, placeholder="Choose your experience")
          


def build_podcast_page():
     st.pills("Podcasts", demo_service.get_podcasts_names(), selection_mode="single", default=None, key=PODCAST_CHOSEN)
     if st.session_state[PODCAST_CHOSEN] != None:
          selected = st.session_state[PODCAST_CHOSEN]
          podcast_info = demo_service.get_podcast_by_name(selected)
          st.button(label="Create Podcast", on_click=handle_podcast_chosen, type="primary")
    
          content_columns = st.columns([3,1])
    
    
          with content_columns[1]:
               with st.container(border=True):
                    col1,col2 = st.columns(2) 
                    col1.image(podcast_info['podcast_logo'],width=200)
                    col2.title(f"{podcast_info['podcast_name']}")
                    col2.write(f"{podcast_info['podcast_tagline']}")
                    st.markdown('**Hosts:**')
                    for host in podcast_info['hosts']:
                         st.write(f"{host['host_name']} ({host['role']})") 
                    st.markdown(f"**Style:**")
                    st.write(podcast_info['writing_style'])
          with content_columns[0]:      
                    if st.session_state[CREATE_STATUS_KEY] == CreateContentStatus.PODCAST_CREATE:
                         with st.container(border=True):
                              with st.spinner("Creating your content"):
                                   
                                   script = content_service.create_podcast_content(podcast_info, input_content_str)
                                   output_file = f"media/podcast-{time.time()}.mp3"
                                   language = "en-gb"
                                   voice = "en-GB-Neural2-B"
                                   audio_service.synthesize_text(text=script,output=output_file, voice_name=voice, language_code=language)

                                   st.title('Podcast Script Draft')
                                   st.audio(output_file)
                                   st.write(script)

def build_newsletter_page():
     st.title('Newsletter creation')
     st.pills("Personas", demo_service.get_personas_names(), selection_mode="single", default=None, key=PERSONA_CHOSEN)

     if st.session_state[PERSONA_CHOSEN] != None: 
          persona_info = demo_service.get_persona_by_name(st.session_state[PERSONA_CHOSEN])
          st.button(label="Create Newsletter", on_click=handle_newsletter_chosen, type="primary")
          col1, col2 = st.columns([2,1])
          with col2:
               with st.container(border=True):
                    st.title(persona_info['name'])
                    #all values of the user in text
                    st.write('What the user values')
                    for entry in persona_info['values']:
                         st.markdown(f"*  {entry['value']}")
                    st.write('What the user is concerned about')
                    for entry in persona_info['concerns']:
                         st.markdown(f"*  {entry['concern']}")
          with col1:
               if st.session_state[CREATE_STATUS_KEY] == CreateContentStatus.NEWSLETTER_OPTIONS:
                    st.write('Choose a persona to personalize your newsletter')
               elif st.session_state[CREATE_STATUS_KEY] == CreateContentStatus.NEWSLETTER_CREATE:
                    with st.spinner('Creating your newsletter'):
                         newsletter = content_service.create_newsletter_content(persona_info, input_content_str)
                         st.html(newsletter)
     else:
          st.write('Choose a persona to customize your newsletter to.')

def build_page():
     if len(st.session_state[LAUNCHPAD_ITEMS]) ==0:
           st.write('Add items to your launchpad before generating content.')
     else:
          cols = st.columns([2,1,2])
          cols[1].metric("Launchpad Items", len(st.session_state[LAUNCHPAD_ITEMS]))
          current_option = st.session_state[CREATE_CHOSEN_OPTION]
          build_creation_options()
          if current_option == CREATE_PODCAST_OPTION:
               build_podcast_page()
          elif current_option == CREATE_NEWSLETTER_OPTION:
               build_newsletter_page()
      
build_page()