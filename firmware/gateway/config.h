#pragma once

// ================================================================
// 集約M5Stack（教壇常設）の設定 — データ契約v1
// ================================================================

#define SCHEMA_VERSION 1
#define WIFI_CHANNEL   1              // ESP-NOWチャンネル。ノード側と一致必須

#define NODE_COUNT 4
static const char *NODE_IDS[NODE_COUNT] = {"n1", "n2", "n3", "n4"};

// 校正オフセット[℃]（8/25の並走校正で決めた値を入れる。表示にのみ適用。
// SDのCSVには生値を記録する＝生データを汚さない）
static const float CAL_OFFSET_T[NODE_COUNT] = {0.0f, 0.0f, 0.0f, 0.0f};

#define LOG_PATH   "/LOG.CSV"         // SDカード上のログ（1受信=1行追記）
#define STALE_MS   90000UL            // 90秒(3周期)受信なしで「無応答」表示
#define SD_CS_PIN  4                  // M5Stack BasicのTFカードCS
