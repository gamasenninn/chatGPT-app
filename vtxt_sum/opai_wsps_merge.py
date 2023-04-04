import openai
import sys
import os
from dotenv import load_dotenv
import pandas as pd

def transcribe_audio(filename):
   
    with open(filename, "rb") as file:
        params ={
            "response_format" : "vtt",
            "temperature" : 0, 
            "language" : "ja"
        }
        transcription = openai.Audio.transcribe("whisper-1", file, **params)
        #print("trans:",transcription)
        #return transcription.text
        return transcription

def main():
    # OpenAI APIキーを設定
    load_dotenv()
    openai.api_key = os.environ["OPEN_API_KEY"]

    # コマンドライン引数または標準入力からファイル名を取得
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("ファイル名を入力してください:").strip()

    # 音声ファイルを文字起こし(L)
    filename_L = filename+'_L.m4a' 
    transcription_text_L = transcribe_audio(filename_L)
    df_L = parse_vtt(transcription_text_L,'L')
    # 音声ファイルを文字起こし(R)
    filename_R = filename+'_R.m4a' 
    transcription_text_R = transcribe_audio(filename_R)
    df_R = parse_vtt(transcription_text_R,'R')
    #print(df_R)
    df_LR = pd.concat([df_L, df_R], ignore_index=True)
    sorted_df = df_LR.sort_values("Start_Time")

    for index, row in sorted_df.iterrows():
    #    #print(f"Row {index}:")
        print(row['Start_Time'],row['LR'],row['Text'])


def parse_vtt(content,LR):
    cues = content.strip().split("\n\n")[1:]
    time_ranges = []
    texts = []

    for cue in cues:
        lines = cue.strip().split("\n")
        #print(f"lines:{lines}")

        if len(lines) == 3:
            _, time_range, text = lines
        else:
            time_range, text = lines
        start_time, end_time = time_range.split(" --> ")

        time_ranges.append((start_time, end_time))
        texts.append(text)

    data = {
        "Start_Time": [start_time for start_time, _ in time_ranges],
        "End_Time": [end_time for _, end_time in time_ranges],
        "LR":LR,
        "Text": texts
    }
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":

    print("文字起こしを開始します・・・・・\n")
    main()

