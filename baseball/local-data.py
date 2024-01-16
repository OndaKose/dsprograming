import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('local-data.csv', encoding='utf-8')

# pandasのデータフレームを確認する
print(df)

import sqlite3

# SQLiteデータベースに接続 (存在しない場合は新しく作成される)
conn = sqlite3.connect('example.db')

# データベースにデータフレームを書き込む (テーブル名を 'baseball_data' とする)
df.to_sql('baseball_data', conn, if_exists='replace', index=False)

# 接続を閉じる
conn.close()