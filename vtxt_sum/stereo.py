import openai
import os

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPEN_API_KEY"]

# Transcribe the stereo audio file
with open("sample.m4a", "rb") as f:
    audio_data = f.read()

infile = "sample.m4a"
with open(infile, "rb") as file:
    params ={
        "response_format" : "verbose_json",
        "temperature" : 0, 
        "language" : "ja" ,
        "prompt": 
            "文字起こししたテキストの先頭に●を付与してください"
    }
    transcription = openai.Audio.transcribe("whisper-1", file, **params)
    print(dir(transcription))

#print("trans:",transcription)
#transcription = openai.Audio.transcribe("whisper-1", audio_data, response_format="vtt")

# Get the text for the left channel
left_channel_text = "\n".join([line.text for line in transcription.lines if line.channel == "L"])
