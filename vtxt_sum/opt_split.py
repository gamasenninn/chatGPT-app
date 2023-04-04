import openai
import os
from dotenv import load_dotenv
from pydub import AudioSegment

# Set up OpenAI API key
load_dotenv()
openai.api_key = os.environ["OPEN_API_KEY"]

# Load input file
infile = "sample02.m4a"
audio = AudioSegment.from_file(infile)

base_name, ext = os.path.splitext(os.path.basename(infile))

# Split audio channels and export them to separate files
for i, channel in enumerate(audio.split_to_mono()):
    filename = f"{base_name}_{'L' if i == 0 else 'R'}.mp3"  # determine output filename
    channel.export(filename, format="mp3")

# Transcribe left channel audio
with open(f"{base_name}_L.mp3", "rb") as file:
    try:
        transcription = openai.Audio.transcribe("whisper-1",file)
        print(transcription['text'])
    except Exception as e:
        print(f"Error occurred during transcription: {str(e)}")