import pandas as pd
import streamlit as st

import constants
from pages.common.common_components import CommonComponents
from services.storage_service import StorageService
import ui_constants
from utils import add_logo
import utils

CommonComponents.init_app()

my_logo = utils.add_logo()

header_row = st.columns([6,1], vertical_alignment="center")
header_row[0].title("Architecture")
header_row[1].image(my_logo)   

st.write("""
        Here you'll find: 
        1.  [Ingestion Pipeline](#ingestion-pipeline) detailing the steps to create the metadata.
        2.  [Prompts](#prompts) with all the inputs sent to gemini models.
        3.  [Metadata](#metadata) format for the different media types.
         
        All the code can be found in this github rep [https://github.com/pedroccorreia/metadata_explorer/](https://github.com/pedroccorreia/metadata_explorer/)
         """)

st.header("Ingestion Pipeline")
st.image('media/architecture.png', caption="Simplified ingestion pripeline for Editorial Solaris")
st.write(
    """
    Steps overview: 

    1.  User uploads different asset types into a google cloud storage bucket.
    2.  Use Colab Enterprise to run the pipeline that generates the metadata.
    3.  The pipeline will run multiple prompts to Gemini to create data according to the asset type. It will also use the Speech to Text to transcribe the audio.
    4.  Those prompts will use the assets provided in step 1. 
    5.  Throughout the different steps it will store metadata into firestore. 
    6.  Transcription files and sub-clips objects are stored in an output folder.    
"""
)

st.header("Prompts")
st.write(" Throughout steps 4, multiple prompts run for the different asset types. Below is an overview of those prompts.")

st.subheader("Videos")
st.text("""For all the videos that were added, three prompts are used in Gemini:
         
1.  Create the summary, long summary, and a list of labels to describe the content;
2.  Choose 3 thumbnails;
3.  List out the key moments in the video. """)

st.write("**Videos - 1. Summary**")
st.code("""
  prompt = \"\"\"SYSTEM:```You are a skilled video analysis expert. You have a deep understanding of media. Your task is to analyze the provided video and extract key information.```
  INSTRUCTION: ```Please analyze the following video and provide long summary, short summary, subject topics.Please format your response as a JSON object with the given structure. Avoid any additional comment or text.```
  OUTPUT:```=
  JSON
  {
    "short_summary": "[One paragraph summary of the content]",
    "long_summary": "[two-three paragraph summary of the content]",
    "subject_topics" :
      [     { "topic": "[topic]"}, { "topic": "[topic]"} ]
  }```
  \"\"\"
""")

st.write("**Videos - 2. Thumbnails**")
st.code("""
  prompt = \"\"\"SYSTEM:```You are a skilled video analysis expert. You have a deep understanding of media and can accurately identify key moments in a video. Your task is to analyze the provided video and extract key thumbnails.```
  INSTRUCTION: ```Give me the timestamp for 3 suitable thumbnails for this video that highlight the key moments.
  Do not add any additional text.```
  OUTPUT:```
  JSON
    "thumbnails": [
      {
        "reason": "[Why this would be a suitable thumbnail for the video]",
        "time": "[mm:ss]",

      },
      {
        "reason": "[Why this would be a suitable thumbnail for the video]",
        "time": "[mm:ss]",
      }
    ]
  ```
  \"\"\"
""")

st.write("**Videos - 3. Chapterization**")
st.code(""" 
 text1 = \"\"\"SYSTEM:```You are a skilled video analysis expert. You have a deep understanding of media and can accurately identify key moments in a video. Your task is to analyze the provided video and extract all the highlight clips. For each clip, you need to classify the type of highlight and provide the precise start and end timestamps.```
  INSTRUCTION: ```Please analyze the following video and provide a list of all the highlight clips with their type and timestamps. Also explain the reason why the selection of that particular timestamp has been made. Please format your response as a JSON object with the given structure. Make sure the audio is not truncated while suggesting the clips. Avoid any additional comment or text.```
  OUTPUT:```
  JSON
  {
    "sections": [
      {
        "type": "[highlight type]",
        "start_time": "[mm:ss]",
        "end_time": "[mm:ss]",
        "reason" : ""
      },
      {
        "type":"[highlight type]",
        "start_time": "[mm:ss]",
        "end_time": "[mm:ss]",
        "reason" : ""
      }
    ]
  }```
  Please make sure the timestamps are accurate and reflect the precise start and end of each highlight clip.\"\"\"

""")


st.subheader("Images")

st.write("""For all the images that were added, one prompts is used in Gemini: Create the summary, long summary, and a list of labels to describe the content.""")
st.write("**Images - 1. Summary**")
st.code("""
prompt = \"\"\"SYSTEM:```You are a skilled image analysis expert. You have a deep understanding of media. Your task is to analyze the provided image and extract key information.```
  INSTRUCTION: ```Please analyze the following image and provide a description, subject topics, photo type, persons.Please format your response as a JSON object with the given structure. Avoid any additional comment or text.```
  OUTPUT:```=
    JSON
  {
    "description": "[A one line description that would support understanding the contents of the image]",
    "photo_type": "[Type of angles used to take the photography]",
    "location" : "A description of the location where the shot is taken, or if it is a known sight, its name",
    "subject_topics" :
      [     { "topic": "[topic]"}, { "topic": "[topic]"} ]
    "persons" :
  [     { "person": "[person1]"}, { "person": "[person2]"} ]
  }```
  \"\"\"
""")




st.subheader("Audio")
st.write("""For all the audio files that were added, one prompts is used in Gemini: Get the show name, Create the summary, long summary, and a list of labels to describe the content.""")
st.write("**Audio - 1. Summary**")
st.code("""
  prompt = \"\"\"SYSTEM:```You are a skilled podcast expert. You have a deep understanding of media. Your task is to analyze the provided audio and extract key information.```
  INSTRUCTION: Please analyze the following video and provide long summary, short summary, subject topics.Please format your response as a JSON object with the given structure. Avoid any additional comment or text.
  OUTPUT:```=
  JSON
  {
    "show_name" : "the name of the podcast show"
    "short_summary": "[One paragraph summary of the content]",
    "long_summary": "[two-three paragraph summary of the content]",
    "subject_topics" :
      [     { "topic": "[topic]"}, { "topic": "[topic]"} ]
  }```
  \"\"\"
""")

st.header("Metadata")
st.subheader("Videos")

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
