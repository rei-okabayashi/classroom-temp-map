"""使いたい場合はpython, pandas, matplotlibのインストールが必要です。
1, analysisフォルダのREADMEに従ってonmura.dbを作成します。この際csvは"LOG.CSV"という名前じゃないと作成してくれません。
2, df = pd.read_sqlから始まる4行は各ノードを示しており、それぞれ時間範囲(recv_time)を合わせる必要があります。
3, 実行を押すとグラフが表示されます。
"""



import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
import sqlite3
from pathlib import Path
import sys

DB = Path(__file__).resolve().parent / "onmura.db"   # このファイルと同じフォルダのDBを見る
conn = sqlite3.connect(DB)   # データベースと接続



#時間とノードでフィルタをかけ、ノード、温度、時間を取得
df = pd.read_sql("SELECT node_id, temp_c, recv_time FROM readings where node_id = 'n1' and recv_time > '2026-08-25 08:00:00' and recv_time < '2026-08-25 16:00:00' order by recv_time", conn)
df2 = pd.read_sql("SELECT node_id, temp_c, recv_time FROM readings where node_id = 'n2' and recv_time > '2026-08-25 08:00:00' and recv_time < '2026-08-25 16:00:00' order by recv_time", conn)
df3 = pd.read_sql("SELECT node_id, temp_c, recv_time FROM readings where node_id = 'n3' and recv_time > '2026-08-25 08:00:00' and recv_time < '2026-08-25 16:00:00' order by recv_time", conn)
df4 = pd.read_sql("SELECT node_id, temp_c, recv_time FROM readings where node_id = 'n4' and recv_time > '2026-08-25 08:00:00' and recv_time < '2026-08-25 16:00:00' order by recv_time", conn)

conn.close() #データベースを閉じる


plt.rcParams["font.family"] = "Yu Gothic"   #フォントの指定 AI生成

#データが空だった場合にプログラムを終了させ、メッセージを出力。
if df.empty:
    sys.exit("その条件のデータがありません。node_idと時間範囲を確認してください。")


df["recv_time"] = pd.to_datetime(df["recv_time"]) #pandasで扱うため時間のデータ型に変換 AIの提案ほぼそのまま
df2["recv_time"] = pd.to_datetime(df2["recv_time"])
df3["recv_time"] = pd.to_datetime(df3["recv_time"])
df4["recv_time"] = pd.to_datetime(df4["recv_time"])

#.plotは折れ線グラフを描画するための関数。引数(時間データ(5個おき)x軸に、温度データ(5個おき)をy軸に、折れ線の色、ラベル名 [::5]の部分はAIで知る
plt.plot(df["recv_time"].iloc[::5], df["temp_c"].iloc[::5], color = "g", label = df["node_id"].iloc[0])
plt.plot(df2["recv_time"].iloc[::5], df2["temp_c"].iloc[::5], color = "r", label = df2["node_id"].iloc[0])
plt.plot(df3["recv_time"].iloc[::5], df3["temp_c"].iloc[::5], color = "b", label = df3["node_id"].iloc[0])
plt.plot(df4["recv_time"].iloc[::5], df4["temp_c"].iloc[::5], color = "y", label = df4["node_id"].iloc[0])


plt.legend() #ラベルを画面に表示

plt.xlabel("time", color = 'g', fontstyle = 'italic')   #x軸のラベルの設定
plt.ylabel("temperature", color = 'g', fontstyle = 'italic')    #y軸のラベルの設定


#以下4行は目盛りのちぐはぐな部分をAIに解決してもらったもの。一部自分が書き換えた。
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))      #x軸の目盛りを「時:分」で表示
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))   #2時間間隔で目盛りを表示
plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[0, 15, 30, 45]))   #15分ごとにx軸の補助目盛りを表示

#下記2行は補助目盛りの描画し過ぎを防ぐためにAIとの相談の上追加。というか無いとダメだった。
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))    #y軸の主目盛りの設定
plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(0.5))  #y軸の補助目盛りの設定

ticks = list(plt.gca().get_xticks())    #x軸の要素(今回時間のデータ)を内部的な数値に変換し、リストとして取得
ticks = [mdates.date2num(df["recv_time"].iloc[0])] + ticks + [mdates.date2num(df["recv_time"].iloc[-1])] #ticksに列の最初の要素と最後の要素を追加(目盛りの最初と最後を表示したい)


#print(ticks)
plt.xticks(ticks)   #最終的な目盛りの表示の設定

plt.grid(axis = 'x', which = 'major', linestyle = '-')                  #グラフ背景の主線の設定 x軸
plt.grid(axis = 'y', which = 'major', linestyle = '-')                  #グラフ背景の主線の設定 y軸

plt.grid(axis = 'x', which = 'minor', linestyle = '--', alpha = 0.5)    #グラフ背景の補助線の設定 x軸
plt.grid(axis = 'y', which = 'minor', linestyle = '--', alpha = 0.5)    #グラフ背景の補助線の設定 y軸
#plt.yticks([22, 23, 24, 25, 26, 27, 28, 29, 30])
plt.tick_params(direction = 'inout', which = 'both')    #目盛りの設定 direction = inout:目盛りが外枠にかかる設定 which = both:主目盛り、補助目盛り両方

plt.margins(x = 0, y = 0)   #デフォルトで設定された余白をなくすためのもの

plt.ylim(18, 36)    #y軸の幅　今回18～36度


plt.title("教室の温度推移")    #グラフのタイトル 


plt.show()


