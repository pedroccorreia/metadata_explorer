import json
from google.cloud import storage

import constants

# Function that converts the json object with the topics into a simple array with the strings 
# of the different topics
def get_labels(labels):
    res = []
    for label in labels:
        res.append(label['topic'])
    return res

# Converts a gcs uri into its url
def get_public_gcs_url(gcs_uri: str) -> str:
    """Transforms a GCS URI to a public URL.

Args:
    gcs_uri: The GCS URI in the format 'gs://bucket-name/path/to/file'.

Returns:
    The public URL for the GCS object.
"""
    bucket_name = gcs_uri.split('/')[2]
    object_path = '/'.join(gcs_uri.split('/')[3:])
    return f"https://storage.cloud.google.com/{bucket_name}/{object_path}"

# Code to convert the response of the transcription results of the api (https://cloud.google.com/speech-to-text/) into a VTT file (https://en.wikipedia.org/wiki/WebVTT)
def json_to_vtt2(json_data, output_file):
    """Converts a JSON transcript object to a VTT file with 6-8 word bundles.

    Args:
        json_data (dict): The JSON data containing the transcript.
        output_file (str): The name of the output VTT file.
    """

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('WEBVTT\n\n')

        for result in json_data['results']:
            for alternative in result['alternatives']:
                words = alternative['words']

                # Bundle words into groups of 8
                for i in range(0, len(words), 12):  # Start at 0, increment by 8
                    bundle = words[i:i+12]  # Take up to 8 words

                    if bundle:  # Check if the bundle is not empty
                        start = bundle[0]['startOffset']
                        end = bundle[-1]['endOffset']
                        text = ' '.join(word['word'] for word in bundle)

                        f.write(f'{format_timestamp(start)} --> {format_timestamp(end)}\n')
                        f.write(f'{text}\n\n')

def format_timestamp(timestamp_str):
    """Formats a timestamp string (e.g., '30.240s') to VTT format (HH:MM:SS.mmm).

    Args:
        timestamp_str (str): The timestamp string.

    Returns:
        str: The formatted timestamp.
    """

    # Remove 's' from the end and convert to float
    seconds = float(timestamp_str[:-1])  
    
    # Calculate hours, minutes, seconds, and milliseconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)

    # Return the formatted timestamp string
    return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{milliseconds:03d}'


def load_json_from_gcs_uri(uri):
    """Loads a JSON file from a GCS bucket using its URI.

    Args:
        uri (str): The GCS URI of the JSON file (e.g., 'gs://your-bucket-name/path/to/your/transcript.json').

    Returns:
        dict: The loaded JSON data.
    """

    storage_client = storage.Client()
    bucket_name = uri[5:].split('/')[0]  # Extract bucket name from URI
    blob_name = '/'.join(uri[5:].split('/')[1:])  # Extract blob name from URI
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    json_string = blob.download_as_string()
    return json.loads(json_string)

def get_transcription_detail(json_data):
    # Extract and concatenate transcripts
    final_transcript = ''
    transcripts = []
    for result in json_data['results']:
      if 'alternatives' in result:
        for alternative in result['alternatives']:
            if 'transcript' in alternative:
              transcripts.append(alternative['transcript'])
    if transcripts:
      final_transcript = ' '.join(transcripts)            
    return final_transcript


def get_bytes_from_gcs(gcs_uri):
  """Fetches bytes from a GCS URI.

  Args:
      gcs_uri: The Google Cloud Storage URI of the assets (e.g., 'gs://your-bucket-name/path/to/image.jpg')

  Returns:
      bytes: The bytes if successful, otherwise None.
  """

  try:
      # Parse the GCS URI
      bucket_name = gcs_uri.replace("gs://", "").split("/")[0]
      blob_name = "/".join(gcs_uri.replace("gs://", "").split("/")[1:])

      # Authenticate to GCS
      storage_client = storage.Client()

      # Get the bucket and blob
      bucket = storage_client.bucket(bucket_name)
      blob = bucket.blob(blob_name)

      # Download    1.  github.com github.com image into memory
      image_bytes = blob.download_as_bytes()

      return image_bytes

  except Exception as e:
      print(f"Error fetching image from GCS: {e}")
      return None
  
# Returns the bytes for the video thumbnails
# Currently only 3 thumbnails are generated
def get_thumbnails(video):
    name = video['name']

    # Assuming get_image_from_gcs is your function from the previous example
    return [
        get_bytes_from_gcs(f'gs://{constants.OUTPUT_BUCKET}/thumbnails/{name}_thumbnail_{i}.png') 
        for i in range(0, 3)
    ]