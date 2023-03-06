import openai
import sys
import csv
import os
from dotenv import load_dotenv
import ftplib

# OpenAI APIキーを設定
load_dotenv()
openai.api_key = os.environ["OPEN_API_KEY"] 

# 要約するテキストを指定
text = ''
# モードの選択　chatGPTかそれ以外か

# SP2TXTが存在するディレクトリ
file_dir = os.environ["LOCAL_FILE_DIR"]

def summarize_text(text):
    print("selected chatGPT")
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "スタッフと顧客との電話でのやりとりです。内容の重要なポイントを箇条書きで3～5つあげてください。そのさい型式や金額などの情報があればそれを加えてください。"
#                        "content": "スタッフと顧客との電話でのやりとりです。なるべく1文で要約してください。そのさい型式や金額や顧客の名前などの情報があればそれを加えてください。"
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
        )

    # 要約されたテキストを取得
    summary = response.choices[0].message.content.strip()
    return summary

def read_text(file_path):
    src_text = ''
    with open(file_path, newline='', encoding='cp932') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            #print(row[0],row[4])
            src_text +=  f"{row[0]}: {row[4]}\n"
    print(src_text)
    return src_text

def write_sum_text(file_path,text):
    src_text = ''
    with open(file_path,  'w' ,encoding='cp932') as wf:
        wf.write(text)

def upload_to_server(file_name):
    # FTPサーバーに接続する
    ftp_url = os.environ["FTP_SERVER_URL"]
    ftp_user_id = os.environ["FTP_USER_ID"]
    ftp_pass = os.environ["FTP_PASSWORD"]
    remote_file_path = f'{os.environ["REMOTE_FILE_DIR"]}/{file_name}'
    local_file_path = os.path.join(os.environ["LOCAL_FILE_DIR"],file_name)

    ftp = ftplib.FTP(ftp_url)
    ftp.set_pasv('true')
    ftp.login(ftp_user_id, ftp_pass)

    #ftp.cwd(f'{os.environ["REMOTE_FILE_DIR"]}')
    #files = ftp.nlst()
    #print("files:",files)

    ## バイナリモードでファイルを開く
    #print("remote_file:",remote_file_path)
    with open(local_file_path, "rb") as file:
        # FTPサーバーにファイルをアップロードする
        #print("uploding......")
        ftp.storbinary(f"STOR {remote_file_path}", file)

    ftp.quit()    



if __name__ == "__main__":


    if len(sys.argv) > 1 :       
        file_path = os.path.join(file_dir,f"txt_{sys.argv[1]}.csv")
        src_text = read_text(file_path)
        sum_text = summarize_text(src_text)
        print(sum_text)
    else:
        while True:
            fid = input("\nパラメータ=文書番号を指定してください")
            file_name = f"txt_{fid}.csv"
            file_path = os.path.join(file_dir,file_name)
            src_text = read_text(file_path)
            sum_text = summarize_text(src_text)
            print(sum_text)
            sum_file_name = f"sum_{fid}.txt"
            wfile_path = os.path.join(file_dir,sum_file_name)
            write_sum_text(wfile_path,sum_text)    
            upload_to_server(sum_file_name)
        


    
