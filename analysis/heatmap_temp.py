"""今回のコードは時間の制約もあり、大半をAIに助けてもらいました。
基本的に自分のコードのを見てもらい、対話の中で足りないところやうまく動作していない部分の改善案を提案してもらいましたが、結果的に自分のコードはほとんど書き換えることになりました。
使用方法はanalysis/README.mdに記載します"""



import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
import sqlite3
from pathlib import Path
import sys

DB = Path(__file__).resolve().parent / "onmura.db"   # このファイルと同じフォルダのDBを見る
conn = sqlite3.connect(DB)   # データベースと接続

#時間とノードでフィルタをかけ、ノード、温度、時間を取得し、時間順に並べる。
df = pd.read_sql("SELECT node_id, temp_c, recv_time FROM readings where recv_time > '2026-08-25 08:00:00' and recv_time < '2026-08-25 16:00:00' order by recv_time", conn)

conn.close()

#データが空だった場合にプログラムを終了させ、メッセージを出力。
if df.empty:
    sys.exit("その条件のデータがありません。node_idと時間範囲を確認してください。")
plt.rcParams["font.family"] = "Yu Gothic"   #フォントの指定 AI生成


df["recv_time"] = pd.to_datetime(df["recv_time"]) #pandasで扱うため時間のデータ型に変換 AIの提案ほぼそのまま



node_names = ["n1", "n2", "n3", "n4"] #AI生成

freqT = "1min" #時間の幅を変数として管理 アイデアをAIとして形にした


#AI生成 データフレームを行をnode_id、列をrecv_timeの表にし、温度を値として管理する。時間範囲(freq)で平均(aggfunc="mean")をとる。
df_pivot = df.pivot_table(index="node_id", columns=pd.Grouper(key = "recv_time", freq = freqT), values="temp_c", aggfunc="mean") 
df_pivot = df_pivot.reindex(node_names) # AI生成　node_namesの順に並べなおす

#AI生成 最大2個まで(limit=2)欠損地を前の値で保管する(.ffill)、
df_pivot = df_pivot.ffill(axis = 1, limit = 2)

#AI生成 列を取得し、2列以上なら時間で引き算を実行。2列未満でもfreqTの値を代入
time_step = (df_pivot.columns[1] - df_pivot.columns[0]) if len(df_pivot.columns) > 1 else pd.Timedelta(freqT)

#AI生成　ヒートマップのマス同士の境界線を設定。列をリストにし、そこに最後の時間＋time_stepをリストに加える。つまりマス＋1の境界線が必要ということ。
x_edges = list(df_pivot.columns) + [df_pivot.columns[-1] + time_step]

#AI生成　ノードの数+1の境界線をY軸に設定
y_edges = range(len(node_names) + 1)

#AI生成　df_pivot.valuesはデータフレームの値のみを二次元配列で取り出す。グラデーション(cmap),温度の上限下限(vmin,vmax),マス目表示(shading="flat"),境界線非表示(edgecolors = "none")
mesh = plt.gca().pcolormesh(x_edges, y_edges, df_pivot.values, cmap="seismic", vmin = 22, vmax = 32, shading="flat", edgecolors = "none", )

#以下2行AI生成　y軸のラベルの位置を真ん中に配置し、ラベル名,色,サイズ,太さを設定。
plt.gca().set_yticks([i + 0.5 for i in range(len(node_names))])
plt.gca().set_yticklabels(node_names, color = "blue", fontsize = 12, fontweight = "bold")


plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))      #x軸の目盛りを「時:分」で表示

plt.title("2026-08-25")


plt.colorbar(mesh, label="温度 (℃)") #AI生成 ヒートマップのデータを横のカラーバーにも反映させる。

plt.tight_layout() #AI生成 余白を自動調整 タイトルやラベルカラーバーなどのはみ出しや被りを避けるため。

plt.show()
