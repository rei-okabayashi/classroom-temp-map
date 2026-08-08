# -*- coding: utf-8 -*-
"""LOG.CSV を SQLite に取り込んで、温度ムラの基本集計を表示する。

使い方（SDカードからコピーした LOG.CSV と同じフォルダで）:
    python log_to_sqlite.py LOG.CSV

出来ること:
  1) onmura.db（SQLite）を作って readings テーブルに取り込む
  2) ノード別の件数・最低/平均/最高気温を表示
  3) 「時間帯 × ノード」の平均気温クロス表を表示（温度ムラが見える）

Python標準ライブラリだけで動く（追加インストール不要）。
時刻未設定（clock=unset）の行は集計から除外する（--include-unset で含められる）。
"""
import csv
import sqlite3
import sys
from pathlib import Path

COLUMNS = ["recv_time", "clock", "node_id", "seq", "temp_c", "hum_pct", "status"]


def load(csv_path: Path, include_unset: bool) -> sqlite3.Connection:
    con = sqlite3.connect("onmura.db")
    con.execute("DROP TABLE IF EXISTS readings")
    con.execute(
        """CREATE TABLE readings (
             recv_time TEXT, clock TEXT, node_id TEXT, seq INTEGER,
             temp_c REAL, hum_pct REAL, status TEXT)"""
    )
    kept = skipped = dup = 0
    last_seq: dict[str, str] = {}  # ノード別の直前採用seq（再送由来の連続重複を除く）
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f"CSVの列が契約と違います。足りない列: {missing}")
        for row in reader:
            if row["status"] != "ok":
                skipped += 1
                continue
            if row["clock"] != "set" and not include_unset:
                skipped += 1
                continue
            # 送達確認のACKだけが失われた場合、ノードは同じseqをもう一度送る（契約の1回再送）。
            # そのとき集約は同一(node_id, seq)を2行記録するので、直前と同じseqだけ捨てる。
            # ノード再起動でseqは0に戻るが、その場合は直前のseqと一致しないので誤って落とさない。
            if last_seq.get(row["node_id"]) == row["seq"]:
                dup += 1
                continue
            last_seq[row["node_id"]] = row["seq"]
            con.execute(
                "INSERT INTO readings VALUES (?,?,?,?,?,?,?)",
                (row["recv_time"], row["clock"], row["node_id"], int(row["seq"]),
                 float(row["temp_c"]), float(row["hum_pct"]), row["status"]),
            )
            kept += 1
    con.commit()
    print(f"取り込み: {kept}行（除外: {skipped}行 = sensor_err / 時刻未設定、再送重複: {dup}行）")
    return con


def per_node(con: sqlite3.Connection) -> None:
    print("\n== ノード別サマリ ==")
    print(f"{'node':>6} {'件数':>6} {'最低':>6} {'平均':>6} {'最高':>6}")
    q = """SELECT node_id, COUNT(*), MIN(temp_c), AVG(temp_c), MAX(temp_c)
           FROM readings GROUP BY node_id ORDER BY node_id"""
    for nid, n, lo, avg, hi in con.execute(q):
        print(f"{nid:>6} {n:>6} {lo:>6.1f} {avg:>6.1f} {hi:>6.1f}")


def hour_by_node(con: sqlite3.Connection) -> None:
    nodes = [r[0] for r in con.execute(
        "SELECT DISTINCT node_id FROM readings ORDER BY node_id")]
    if not nodes:
        return
    print("\n== 時間帯 × ノードの平均気温（℃）==")
    print("  hour " + "".join(f"{n:>7}" for n in nodes) + "   最大差")
    q = """SELECT strftime('%H', recv_time) AS hh, node_id, AVG(temp_c)
           FROM readings GROUP BY hh, node_id"""
    table: dict[str, dict[str, float]] = {}
    for hh, nid, avg in con.execute(q):
        table.setdefault(hh, {})[nid] = avg
    for hh in sorted(table):
        vals = [table[hh].get(n) for n in nodes]
        cells = "".join(f"{v:>7.1f}" if v is not None else f"{'-':>7}" for v in vals)
        present = [v for v in vals if v is not None]
        spread = (max(present) - min(present)) if len(present) >= 2 else 0.0
        print(f"    {hh} {cells} {spread:>7.1f}")
    print("（最大差 = その時間帯で一番暑いノードと一番寒いノードの差。これが温度ムラ）")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    include_unset = "--include-unset" in sys.argv
    csv_path = Path(args[0]) if args else Path("LOG.CSV")
    if not csv_path.exists():
        sys.exit(f"{csv_path} が見つかりません。SDカードのLOG.CSVをここにコピーしてください。")
    con = load(csv_path, include_unset)
    per_node(con)
    hour_by_node(con)
    print("\nonmura.db を作りました。SQLiteの練習: sqlite3 onmura.db で開いて自由に集計できます。")


if __name__ == "__main__":
    main()
