# Load environment dependent variables from yaml file
import yaml
from enum import Enum


with open('config.yaml', 'r') as file:
    config_info = yaml.safe_load(file)


PROJECT_NUMBER = config_info['project']['project_number']
PROJECT_ID = config_info['project']['project_id']
LOCATION= config_info['project']['location']

EMBEDDING_MODEL = config_info['models']['embedding']
CREATION_MODEL = config_info['models']['creation']


OUTPUT_BUCKET = config_info['storage']['output_bucket']
INPUT_BUCKET = config_info['storage']['input_bucket']


VIDEO_FIRESTORE_DATABASE = config_info['db']['video']
IMAGE_FIRESTORE_DATABASE = config_info['db']['image']
AUDIO_FIRESTORE_DATABASE = config_info['db']['audio']
ARTICLE_FIRESTORE_DATABASE = config_info['db']['article']

SEARCH_DEPLOYED_INDEX_ID = config_info['search']['deployed_index_id']
SEARCH_ENDPOINT_ID = config_info['search']['index_endpoint']


SERVICE_ACCOUNT_KEY_FILE = 'secrets/credentials.json'


# VOICE_MODEL = ['voice']['model']

class AssetTypes(Enum):
    ARTICLE = "article"
    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"
    SEGMENT = "segment"