"""使いたい場合はpython, pandas, matplotlibのインストールが必要です。
1, analysisフォルダのREADMEに従ってonmura.dbを作成します。この際csvは"LOG.CSV"という名前じゃないと作成してくれません。
2, df = pd.read_sqlから始まる行の時間範囲(recv_time)を変えればグラフの範囲も変わります。
3, 実行を押すとグラフが表示されます。
4, プログラムの下側plt.show()の手前にコメントアウトしてある行がありますが、これは指定した時間の値を出力させる確認用のものです。気になったらお使いください。

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


#時間とノードでフィルタをかけ、ノード、温度、時間を取得し、時間順に並べる。
df = pd.read_sql("SELECT node_id, temp_c, recv_time FROM readings where node_id = 'n1' and recv_time > '2026-08-24 02:00:00' and recv_time < '2026-08-24 14:00:00' order by recv_time ", conn)

conn.close() #データベースを閉じる

#データが空だった場合にプログラムを終了させ、メッセージを出力。
if df.empty:
    sys.exit("その条件のデータがありません。node_idと時間範囲を確認してください。")


plt.rcParams["font.family"] = "Yu Gothic"   #フォントの指定 AI生成


df["recv_time"] = pd.to_datetime(df["recv_time"]) #pandasで扱うため時間のデータ型に変換 AIの提案ほぼそのまま


#.plotは折れ線グラフを描画するための関数。引数(時間データ(5個おき)x軸に、温度データ(5個おき)をy軸に、折れ線の色、ラベル名 [::5]の部分はAIで知る
plt.plot(df["recv_time"].iloc[::5], df["temp_c"].iloc[::5], color = "g", label = df["node_id"].iloc[0])

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

plt.xticks(ticks)   #最終的な目盛りの表示の設定

plt.grid(axis = 'x', which = 'major', linestyle = '-')                  #グラフ背景の主線の設定 x軸
plt.grid(axis = 'y', which = 'major', linestyle = '-')                  #グラフ背景の主線の設定 y軸

plt.grid(axis = 'x', which = 'minor', linestyle = '--', alpha = 0.5)    #グラフ背景の補助線の設定 x軸
plt.grid(axis = 'y', which = 'minor', linestyle = '--', alpha = 0.5)    #グラフ背景の補助線の設定 y軸

plt.tick_params(direction = 'inout', which = 'both')    #目盛りの設定 direction = inout:目盛りが外枠にかかる設定 which = both:主目盛り、補助目盛り両方

plt.margins(x = 0, y = 0)   #デフォルトで設定された余白をなくすためのもの

plt.ylim(20, 32)    #y軸の幅 今回20～32度


plt.title("教室の温度推移")    #グラフのタイトル

"""target = pd.to_datetime("15:00")
print(df[
    df["recv_time"].dt.strftime("%H:%M") == target.strftime("%H:%M")
])"""

plt.show()


