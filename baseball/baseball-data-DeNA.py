from bs4 import BeautifulSoup
import requests
import sqlite3

# スクレイピングするURLのリスト
urls = [
    "https://nf3.sakura.ne.jp/php/stat_disp/stat_disp.php?y=2022&leg=0&mon=0&tm=DB&vst=all",
    "https://nf3.sakura.ne.jp/php/stat_disp/stat_disp.php?y=0&leg=0&mon=0&tm=DB&vst=all"
]

# データベースファイルに接続
conn = sqlite3.connect('scraped_data.db')
cursor = conn.cursor()

# テーブルの作成
cursor.execute('''
    CREATE TABLE IF NOT EXISTS headers (
        date0 TEXT,
        date1 TEXT,
        head0 TEXT,
        head5 TEXT,
        head15 TEXT,
        head16 TEXT,
        head18 TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        col0 TEXT,
        col1 TEXT,
        col2 TEXT,
        col7 TEXT,
        col17 TEXT,
        col18 TEXT,
        col20 TEXT
    )
''')

for url in urls:
    response = requests.get(url)
    html_soup = BeautifulSoup(response.content, 'html.parser')

# HTMLから必要なデータを抽出するコード
date_elements = html_soup.find_all('tr', class_='Index')
header_elements = html_soup.find_all('tr', class_='Index2')
data_elements = html_soup.find_all('tr', onmouseover="M_over(this)")

if date_elements:
    dates = date_elements[0].find_all('th')
    if len(dates) > 2:  
        date0 = dates[0].text.strip()
        date1 = dates[1].text.strip()

if header_elements:
    heads = header_elements[0].find_all('th')
    if len(heads) > 7:
        head0 = heads[0].text.strip()
        head5 = heads[5].text.strip()
        head15 = heads[15].text.strip()
        head16 = heads[16].text.strip()
        head18 = heads[18].text.strip()

        # ヘッダー情報のデータベースへの挿入
        cursor.execute('''
            INSERT INTO headers (date0, date1, head0, head5, head15, head16, head18)
            VALUES (?, ?, ?, ?, ?, ?,
        ?)
        ''', (date0, date1, head0, head5, head15, head16, head18))

for i in data_elements:
    cols = i.find_all('td')
    if len(cols) > 7:
        col0 = cols[0].text.strip()
        col1 = cols[1].text.strip()
        col2 = cols[2].text.strip()
        col7 = cols[7].text.strip()
        col17 = cols[17].text.strip()
        col18 = cols[18].text.strip()
        col20 = cols[20].text.strip()

        # データ行のデータベースへの挿入
        cursor.execute('''
            INSERT INTO data (col0, col1, col2, col7, col17, col18, col20)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (col0, col1, col2, col7, col17, col18, col20))

# コミットして変更を保存
conn.commit()

conn.close()