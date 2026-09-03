#pragma once

// ================================================================
// 集約M5Stack（教壇常設）の設定 — データ契約v1
// ================================================================

#define SCHEMA_VERSION 1
#define WIFI_CHANNEL   1              // ESP-NOWチャンネル。ノード側と一致必須

#define NODE_COUNT 4
static const char *NODE_IDS[NODE_COUNT] = {"n1", "n2", "n3", "n4"};

// 画面に出す設置場所ラベル（READMEの「ノードと設置場所」表に対応。表示にのみ使う。
// CSVには node_id の n1〜n4 だけを記録するので、ここを変えてもログ形式は変わらない）
//
// 並び順は上の NODE_IDS と同じ。半角英数で LABEL_CHARS 文字以内にすること
// （長い分は画面上で切り捨てられる。標準フォントは日本語を表示できない）。
//                                             n1: 窓側(後ろ)  n2: 窓側(前)  n3: 教卓付近  n4: 廊下側(前)
#define LABEL_CHARS 8
static const char *NODE_LABELS[NODE_COUNT] = {"MADO-ATO", "MADO-MAE", "KYOTAKU", "ROKA-MAE"};

// 校正オフセット[℃]（8/25の並走校正で決めた値を入れる。表示にのみ適用。
// SDのCSVには生値を記録する＝生データを汚さない）
//
// 並び順は上の NODE_IDS と同じ。左から n1, n2, n3, n4 の順に対応する。
// 数値の末尾の f は「小数として扱う」という印なので消さないこと。
//                                            n1     n2     n3     n4
static const float CAL_OFFSET_T[NODE_COUNT] = {0.0f, 0.0f, 0.0f, 0.0f};

#define LOG_PATH   "/LOG.CSV"         // SDカード上のログ（1受信=1行追記）
#define STALE_MS   90000UL            // 90秒(3周期)受信なしで「無応答」表示
#define SD_CS_PIN  4                  // M5Stack BasicのTFカードCS
