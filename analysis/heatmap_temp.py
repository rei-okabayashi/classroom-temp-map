import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
import sqlite3
from pathlib import Path
import sys

DB = Path(__file__).resolve().parent / "onmura.db"   # このファイルと同じフォルダのDBを見る
conn = sqlite3.connect(DB)   # データベースと接続


df = pd.read_sql("SELECT node_id, temp_c, recv_time FROM readings where recv_time > '2026-08-24 08:00:00' and recv_time < '2026-08-24 16:00:00' order by recv_time", conn)

conn.close()

#データが空だった場合にプログラムを終了させ、メッセージを出力。
if df.empty:
    sys.exit("その条件のデータがありません。node_idと時間範囲を確認してください。")
plt.rcParams["font.family"] = "Yu Gothic"   #フォントの指定 AI生成


df["recv_time"] = pd.to_datetime(df["recv_time"]) #pandasで扱うため時間のデータ型に変換 AIの提案ほぼそのまま



node_names = ["n1", "n2", "n3", "n4"]
df_pivot = df.pivot_table(index="node_id", columns=pd.Grouper(key = "recv_time", freq = "5min"), values="temp_c", aggfunc="mean")
df_pivot = df_pivot.reindex(node_names) # ノードの並び順を固定

df_pivot = df_pivot.ffill(axis=1).bfill(axis=1)

time_step = (df_pivot.columns[1] - df_pivot.columns[0]) if len(df_pivot.columns) > 1 else pd.Timedelta(minutes=1)
x_edges = list(df_pivot.columns) + [df_pivot.columns[-1] + time_step]

y_edges = range(len(node_names) + 1)


#plt.pcolor(pd.DataFrame(c).iloc[::-1].T, cmap = "hot_r") #pd.DataFrame(c)はAIに相談の上採用しました。
mesh = plt.gca().pcolormesh(x_edges, y_edges, df_pivot.values, cmap="seismic", shading="flat", edgecolors = "none", )
plt.gca().set_yticks([i + 0.5 for i in range(len(node_names))])
plt.gca().set_yticklabels(node_names, color = "blue", fontsize = 12, fontweight = "bold")


#以下4行は目盛りのちぐはぐな部分をAIに解決してもらったもの。一部自分が書き換えた。
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))      #x軸の目盛りを「時:分」で表示



plt.colorbar(mesh, label="温度 (℃)")

plt.tight_layout() #ai

plt.show()
