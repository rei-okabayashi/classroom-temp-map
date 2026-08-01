# analysis — 運用データの分析（データ分析担当の作業場所）

SDカードの `LOG.CSV` をここにコピーして:

```bash
python log_to_sqlite.py LOG.CSV
```

- `onmura.db`（SQLite）が作られ、ノード別サマリと「時間帯×ノードの平均気温」クロス表が表示される
- **最大差の列が「温度ムラ」そのもの** — 発表の根拠データはここから作る
- 訓練で習ったSQLiteの実践場所。`sqlite3 onmura.db` で開いて自由に集計してよい
- `sample/LOG.CSV` は動作確認用のダミーデータ（実データが無くても試せる）

時刻未設定（clock=unset）の行とセンサーエラー行は自動で除外される（`--include-unset` で含められる）。

## 次の一手の例

- 日別・曜日別の集計を足す
- グラフ化（matplotlib / Excel / Googleスプレッドシート、好きな道具でOK）
- 設置場所ラベル（README の n1〜n4 対応表）と結合して「窓際 vs エアコン直下」で語る
