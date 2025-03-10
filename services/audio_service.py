import vertexai
import constants


from google.cloud import texttospeech_v1beta1 as texttospeech
from google.api_core.client_options import ClientOptions
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig

TTS_LOCATION = "us-central1"
REGION = "us-central1"
DEFAULT_LANGUAGE = "en-au"

class AudioService:

    def __init__(self):
        vertexai.init(project=constants.PROJECT_ID,location=REGION)
        
        self.voice = "en-US-Studio-O" # constants.VOICE_MODEL
        self.tts_client = texttospeech.TextToSpeechClient(
        client_options=ClientOptions(
            api_endpoint=f"{TTS_LOCATION}-texttospeech.googleapis.com"
        )
        )
        self.model = GenerativeModel("gemini-pro")

    def synthesize_text( self,
        text: str, output: str, voice_name: str, language_code: str = DEFAULT_LANGUAGE
    ):
        response = self.tts_client.synthesize_speech(
            input=texttospeech.SynthesisInput(text=text),
            voice=texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name,
            ),
            audio_config=texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            ),
        )

        # The response's audio_content is binary.
        with open(output, "wb") as f:
            f.write(response.audio_content)
        