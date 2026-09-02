import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
import sqlite3
from pathlib import Path
import sys

DB = Path(__file__).resolve().parent / "onmura.db"   # このファイルと同じフォルダのDBを見る
conn = sqlite3.connect(DB)   # データベースと接続

#cur = conn.cursor()
df = pd.read_sql("SELECT node_id, temp_c, recv_time FROM readings where recv_time > '2026-08-25 09:00:00' and recv_time < '2026-08-25 15:00:00' order by recv_time", conn)
#df = pd.read_sql("SELECT node_id, temp_c, recv_time FROM readings where recv_time > '2026-08-22 13:00:00' and recv_time < '2026-08-22 22:00:00' ", conn)




#cur.close()
conn.close()

#データが空だった場合にプログラムを終了させ、メッセージを出力。
if df.empty:
    sys.exit("その条件のデータがありません。node_idと時間範囲を確認してください。")
plt.rcParams["font.family"] = "Yu Gothic"   #フォントの指定 AI生成


df["recv_time"] = pd.to_datetime(df["recv_time"]) #pandasで扱うため時間のデータ型に変換 AIの提案ほぼそのまま

leng_df = len(df["recv_time"]) // 4

n1um = df[df["node_id"] == "n1"]
n2um = df[df["node_id"] == "n2"]
n3um = df[df["node_id"] == "n3"]
n4um = df[df["node_id"] == "n4"]
# index2 = int(leng_df * 0.2)
# index4 = int(leng_df * 0.4)
# index6 = int(leng_df * 0.6)
# index8 = int(leng_df * 0.8)


# c = ([[n1um["temp_c"].iloc[0], n2um["temp_c"].iloc[0], n3um["temp_c"].iloc[0], n4um["temp_c"].iloc[0]],
#      [n1um["temp_c"].iloc[index2], n2um["temp_c"].iloc[index2], n3um["temp_c"].iloc[index2], n4um["temp_c"].iloc[index2]], 
#      [n1um["temp_c"].iloc[index4], n2um["temp_c"].iloc[index4], n3um["temp_c"].iloc[index4], n4um["temp_c"].iloc[index4]],
#      [n1um["temp_c"].iloc[index6], n2um["temp_c"].iloc[index6], n3um["temp_c"].iloc[index6], n4um["temp_c"].iloc[index6]],
#      [n1um["temp_c"].iloc[index8], n2um["temp_c"].iloc[index8], n3um["temp_c"].iloc[index8], n4um["temp_c"].iloc[index8]],
#      [n1um["temp_c"].iloc[leng_df - 2], n2um["temp_c"].iloc[leng_df - 2], n3um["temp_c"].iloc[leng_df - 2], n4um["temp_c"].iloc[leng_df - 2]]
#      ])


nodes = [n1um, n2um, n3um, n4um]
indices = [
    0,
    leng_df // 10 * 2,
    leng_df // 10 * 4,
    leng_df // 10 * 6,
    leng_df // 10 * 8,
    leng_df - 2
]


c = [
    [node["temp_c"].iloc[i] for node in nodes]
    for i in indices
]



plt.pcolor(pd.DataFrame(c).iloc[::-1].T, cmap = "hot_r") #pd.DataFrame(c)はAIに相談の上採用しました。

#以下4行は目盛りのちぐはぐな部分をAIに解決してもらったもの。一部自分が書き換えた。
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))      #x軸の目盛りを「時:分」で表示
#plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))   #2時間間隔で目盛りを表示
#plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[0, 15, 30, 45]))   #15分ごとにx軸の補助目盛りを表示

#下記2行は補助目盛りの描画し過ぎを防ぐためにAIとの相談の上追加。というか無いとダメだった。
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))    #y軸の主目盛りの設定
plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(0.5))  #y軸の補助目盛りの設定

# ticks = list(plt.gca().get_xticks())    #x軸の要素(今回時間のデータ)を内部的な数値に変換し、リストとして取得
# ticks = [mdates.date2num(df["recv_time"].iloc[0])] + ticks + [mdates.date2num(df["recv_time"].iloc[-1])] #ticksに列の最初の要素と最後の要素を追加(目盛りの最初と最後を表示したい)


# print(ticks)
# plt.xticks(ticks)   #最終的な目盛りの表示の設定


plt.show()



#print(n1um["temp_c"].iloc[leng_df // 10 * 2])
#print(n1um["temp_c"].iloc[len(df["recv_time"]) - 1])
#print(len(df["node_id"]) // 4)
#print(n1um["temp_c"].iloc[leng_df // 2])