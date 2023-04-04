import openai
import sys
import csv
import os
from dotenv import load_dotenv
import json
from pydub import AudioSegment
import requests
from openai.api_resources import Audio

# OpenAI APIキーを設定
load_dotenv()
openai.api_key = os.environ["OPEN_API_KEY"] 

# 入力ファイルを読み込みます
infile = "sample.m4a"
audio = AudioSegment.from_file(infile) 

base_name, ext = os.path.splitext(os.path.basename(infile))

# 左右の音声成分を振り分けます
left_channel = audio.split_to_mono()[0]
right_channel = audio.split_to_mono()[1]

# 左右の音声成分をそれぞれのファイルに保存します
left_channel.export(f"{base_name}_L.mp3", format="mp3")
right_channel.export(f"{base_name}_R.mp3", format="mp3")


with open("xample_L.mp3", "rb") as file:
    transcription = openai.Audio.transcribe("whisper-1", file)
    print(transcription.text)


#with open("sample02_R.m4a", "rb") as file:
#    transcription = openai.Audio.transcribe("whisper-1", file)
#    print(transcription.text)
