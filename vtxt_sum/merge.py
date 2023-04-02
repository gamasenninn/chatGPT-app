import pandas as pd

# LとRのファイル名を指定
l_file = 'L_file.vtt'
r_file = 'R_file.vtt'

# ファイルを読み込み、データフレームに変換
l_df = pd.read_csv(l_file, sep='\t', header=None, skiprows=2)
r_df = pd.read_csv(r_file, sep='\t', header=None, skiprows=2)

# 列名を設定
l_df.columns = ['L_Time', 'L_Text']
r_df.columns = ['R_Time', 'R_Text']

# 時刻を datetime 型に変換
l_df['L_Time'] = pd.to_datetime(l_df['L_Time'], format='%H:%M:%S.%f')
r_df['R_Time'] = pd.to_datetime(r_df['R_Time'], format='%H:%M:%S.%f')

# LとRのデータフレームを結合して時系列で並べ替え
merged_df = pd.concat([l_df, r_df], axis=1).sort_values(by=['L_Time', 'R_Time'])

# マージしたデータフレームをCSVファイルに書き出し
merged_df.to_csv('merged_file.csv', index=False)
