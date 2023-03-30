import openai
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from tabulate import tabulate

# OpenAI APIキーを設定
load_dotenv()
openai.api_key = os.environ["OPEN_API_KEY"]

src_text = ''

engine = create_engine('sqlite:///test.db', echo=False)


def gen_sql(text,meta_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature = 0.3,
        messages=[
            {
                "role": "system",
                        "content":  "次のように定義されたテーブルがあります。\n"
                                    f"\n定義データ:\n{meta_text}\n"
                                    "\n"
                                    "これらの定義データにもとづいてユーザからの要求文にもっとも適したSQL文を創成してください。"
                                    "次のようなフォーマットで出力してください。\n"
                                    "説明は100字以内に収めてください\n"
                                    "\n【SQL】\n"
                                    "【説明】\n"
            },
            {
                "role": "user",
                        "content": f"要求文: {text}"
            }
        ],
    )

    return response.choices[0].message.content.strip()


def init_meta_data():

    # メタデータをさくせし、テーブル情報を反映させるためにエンジンからテーブル情報を読み込む
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # メタデータのテーブル情報からテーブル名と列情報を編集する
    meta_text = ''
    for table in metadata.tables.values():
        meta_text += 'テーブル名:'+ table.name + '\n'
        for column in table.columns:
            meta_text += f'列名:{column.name}, 型: {column.type}\n'
        meta_text += '\n'
    return meta_text

def exec_sql(sql):
    Session = sessionmaker(bind=engine)

    try:
        with Session() as session:
            t = text (sql)
            result = session.execute(t)

            header = [k for k in result.keys()]

            rows = result.fetchall()
            tabled = tabulate(rows,header, tablefmt="github")
            print(tabled)

    except SQLAlchemyError as e:
        print(f'Exception Excute SQL: {e}\n')


def repl():

    meta_text = init_meta_data() 
    if not meta_text:
        print("メタデータが入力されていません")
        return
    print('メタデータが読み込まれました\n')
    while True:
        try:
            user_input = input(">")
            if user_input:
                response = gen_sql(user_input,meta_text)
                sql = response.split('【SQL】')[1].split('【')[0].strip()
                sql = sql.replace('```', '').strip()
                description = response.split('【説明】')[1].strip()

                print('SQL文:\n', sql)
                print('説明:\n', description)
                print()

                exec_sql(sql)
                
        except (KeyboardInterrupt, EOFError):
            print()
            break

if __name__ == "__main__":

    repl()
