# Load environment dependent variables from yaml file
import yaml

with open('config.yaml', 'r') as file:
    config_info = yaml.safe_load(file)


PROJECT_NUMBER = config_info['project']['project_number']
PROJECT_ID = config_info['project']['project_id']
LOCATION= config_info['project']['location']


OUTPUT_BUCKET = config_info['storage']['output_bucket']
INPUT_BUCKET = config_info['storage']['input_bucket']


VIDEO_FIRESTORE_DATABASE = config_info['db']['video']
IMAGE_FIRESTORE_DATABASE = config_info['db']['image']
AUDIO_FIRESTORE_DATABASE = config_info['db']['audio']
