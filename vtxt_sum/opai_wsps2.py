import openai
import sys
import os
from dotenv import load_dotenv

def transcribe_audio(filename):
   
    with open(filename, "rb") as file:
        params ={
            "response_format" : "vtt",
            "temperature" : 0, 
            "language" : "ja" ,
            "prompt": 
                "文字起こししたテキストの先頭に●を付与してください"
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

    # 音声ファイルを文字起こし
    transcription_text = transcribe_audio(filename)

    # 文字起こしテキストを標準出力に表示
    print("whisper AI 文字起こし:")
    print(transcription_text)
if __name__ == "__main__":

    print("文字起こしを開始します・・・・・\n")
    main()
    input("\nなにかキーを押してください終了します:")

