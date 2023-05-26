import requests
from decouple import config
import azure.cognitiveservices.speech as speechsdk


AZURE_KEY = config("AZURE_API_KEY")
ENDPOINT = config("AZURE_ENDPOINT")
REGION = config("REGION_KEY")

def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_KEY, region=REGION)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data
        return audio_data
    else:
        return None