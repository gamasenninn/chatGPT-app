from pydub import AudioSegment
import pandas as pd
from datetime import timedelta
import datetime

def detect_speech_nonspeech(audio_path, frame_size=2048, hop_size=512, threshold_ratio=2.5):
    # load audio file
    audio = AudioSegment.from_file(audio_path)
    
    # set frame and hop sizes for analysis
    frame_ms = frame_size / audio.frame_rate * 1000
    hop_ms = hop_size / audio.frame_rate * 1000
    
    # compute RMS for each frame
    rms_list = []
    for i in range(0, len(audio)-frame_size, hop_size):
        frame = audio[i:i+frame_size]
        rms_list.append(frame.rms)
    
    # set threshold for speech/nonspeech classification
    threshold = max(rms_list) / threshold_ratio
    
    # classify frames as speech or nonspeech
    speech_frames = []
    nonspeech_frames = []
    for i in range(len(rms_list)):
        if rms_list[i] > threshold:
            speech_frames.append(i)
        else:
            nonspeech_frames.append(i)
    
    # combine adjacent speech frames into speech segments
    speech_segments = []
    for i in range(len(speech_frames)):
        if i == 0:
            start_frame = speech_frames[i]
        elif speech_frames[i] != speech_frames[i-1]+1:
            end_frame = speech_frames[i-1]
            speech_segments.append((start_frame, end_frame))
            start_frame = speech_frames[i]
    speech_segments.append((start_frame, speech_frames[-1]))
    
    # combine adjacent nonspeech frames into nonspeech segments
    nonspeech_segments = []
    for i in range(len(nonspeech_frames)):
        if i == 0:
            start_frame = nonspeech_frames[i]
        elif nonspeech_frames[i] != nonspeech_frames[i-1]+1:
            end_frame = nonspeech_frames[i-1]
            nonspeech_segments.append((start_frame, end_frame))
            start_frame = nonspeech_frames[i]
    nonspeech_segments.append((start_frame, nonspeech_frames[-1]))
    
    # convert frame indices to milliseconds
    speech_segments_ms = [(s * hop_ms, e * hop_ms) for (s, e) in speech_segments]
    nonspeech_segments_ms = [(s * hop_ms, e * hop_ms) for (s, e) in nonspeech_segments]
    # convert milliseconds to datetime
    #speech_segments_time = [(datetime.timedelta(milliseconds=s), datetime.timedelta(milliseconds=e)) for (s, e) in speech_segments_ms]
    #nonspeech_segments_time = [(datetime.timedelta(milliseconds=s), datetime.timedelta(milliseconds=e)) for (s, e) in nonspeech_segments_ms]    
    # create DataFrame with segment information
    data = {"start_time": [], "end_time": [], "segment_type": []}
    for (start_time, end_time) in speech_segments_ms:
        data["start_time"].append(start_time)
        data["end_time"].append(end_time)
        data["segment_type"].append("speech")
    for (start_time, end_time) in nonspeech_segments_ms:
        data["start_time"].append(start_time)
        data["end_time"].append(end_time)
        data["segment_type"].append("nonspeech")

    df = pd.DataFrame(data)
    df["start_time"] = df["start_time"].apply(lambda x: str(datetime.timedelta(milliseconds=x)))
    df["end_time"] = df["end_time"].apply(lambda x: str(datetime.timedelta(milliseconds=x)))
   
    return df


df = detect_speech_nonspeech("sample02_L.m4a")
print(df)