import openai
import sys
import csv
import os
from dotenv import load_dotenv
import json

# OpenAI APIキーを設定
load_dotenv()
openai.api_key = os.environ["OPEN_API_KEY"] 

with open("sample02_L.m4a", "rb") as file:
    transcription = openai.Audio.transcribe("whisper-1", file)
    print(transcription.text)

with open("sample02_R.m4a", "rb") as file:
    transcription = openai.Audio.transcribe("whisper-1", file)
    print(transcription.text)
