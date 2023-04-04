import openai
import sys
import csv
import os
from dotenv import load_dotenv
import json

# OpenAI APIキーを設定
load_dotenv()
openai.api_key = os.environ["OPEN_API_KEY"] 



with open("36655.m4a", "rb") as file:
    params ={
        "response_format" : "vtt",
        "temperature" : 0, 
        "language" : "ja",
        "prompt":"中古農機具店での電話のやりとり"
    }

    transcription = openai.Audio.transcribe("whisper-1", file,**params)
    print(transcription)

#with open("sample02_R.m4a", "rb") as file:
#    transcription = openai.Audio.transcribe("whisper-1", file)
#    print(transcription.text)
