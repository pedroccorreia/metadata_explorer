import streamlit as st
import constants
import pandas as pd

from services.storage_service import StorageService
import ui_constants


st.set_page_config(
    page_title="Metadata Explorer",
    page_icon="🗺️",
    layout="wide",    
)

if ui_constants.SERVICE_STORAGE not in st.session_state:
    with st.spinner('Getting your experience ready...'):
        # Services initialization
        st.session_state[ui_constants.SERVICE_STORAGE] = StorageService([constants.INPUT_BUCKET, constants.OUTPUT_BUCKET], constants.SERVICE_ACCOUNT_KEY_FILE)



# Page definition
st.header("Metadata Explorer 🗺️")
st.write("This app allows you to explore the metadata of your media assets. There is an ingestion pipeline that looks at your media assets and creates metadata")
st.write("This front end connects to a firestore database that has the metadata on your assets. What's on these assets is explained next.")

st.subheader("Videos")

st.text("""For all the videos that were added, three prompts are used in Gemini:
         
-  Create the summary, long summary, and a list of labels to describe the content;
-  Choose 3 thumbnails;
-  List out the key moments in the video.
        
Here is a the metadata model for videos:
          """)

# Create the pandas DataFrame for video metadata
df_video = pd.DataFrame({
    'Column Name': ['Short Summary', 'Long Summary', 'Labels', 'Thumbnails', 
                    'Key Moments: Shot Type', 'Key Moments: Order',
                    'Key Moments: Reason', 'Key Moments: Start Timestamp',
                    'Key Moments: End Timestamp', 'Key Moments: Transcript'],
    'Description': [
        'A concise and brief overview of the video content.',
        'A detailed and comprehensive summary of the video content.',
        'Keywords or tags associated with the video.',
        'A list of thumbnails for the video.',
        'The type of shot used for the key timestamp '
        'The type of shot used for the key moment (e.g., close-up, landscape).',
        'The order or sequence of the key moment within the video.',
        'The reason why this moment is considered key or important.',
        'The timestamp in the video where the key moment starts.',
        'The timestamp in the video where the key moment ends.',
        'The speech to text transcript.'
    ]
})

# Use st.table to display the DataFrame
st.table(df_video.set_index(df_video.columns[0]))

st.subheader("Images")

st.write("""For all the images that were added, one prompts is used in Gemini: Create the summary, long summary, and a list of labels to describe the content.""")

# Create the pandas DataFrame for image metadata
df_image = pd.DataFrame({
    'Column Name': ['Description', 'Photo Shot Type', 'Location', 'Labels', 'People'],
    'Description': [
        'A textual description of the image content.',
        'The type of shot used (e.g., close-up, landscape, portrait).',
        'The place where the photo was taken.',
        'Keywords or tags associated with the image.',
        'Names or descriptions of people present in the image.'
    ]
})

# Use st.table to display the DataFrame
st.table(df_image.set_index(df_image.columns[0]))

st.subheader("Audio")

# Create the pandas DataFrame
audio_df = pd.DataFrame({
    'Column Name': ['Long Summary', 'Short Summary', 'Labels', 'Transcript'],
    'Description': [
        'A detailed and comprehensive summary of the content.',
        'A concise and brief overview of the content.',
        'Keywords or tags associated with the content.',
        'The transcript of the audio content.'
    ]
})

# Use st.table to display the DataFrame
st.table(audio_df.set_index(audio_df.columns[0]))

