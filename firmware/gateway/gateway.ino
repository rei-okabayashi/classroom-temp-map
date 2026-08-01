// ================================================================
// 教室の温度ムラ「見える化」 集約側（M5Stack Basic・教壇常設）
//
// 役割: 各ノードからESP-NOWでJSONを受信し、
//   1) 画面にリアルタイム表示（校正オフセット適用後の値）
//   2) SDカードの /LOG.CSV に生値を1行追記（1行ごとにflush）
// データ契約v1（docs/data-contract.md）準拠。
//
// 時刻設定: PCとUSB接続し、シリアルモニタ(115200)から
//   TIME 2026-08-17 09:00:00
// と送ると時計が設定される。設定するまで画面に「時刻未設定」警告。
//
// ※これは企画者が用意した「動く骨組み」。ここから先が集約表示オーナーの領分:
//   画面レイアウトの改善・日本語表示・しきい値アラート(色)・校正値の反映・
//   時刻運用の改善・ミニグラフ など(docs/backlog.md参照)。
//
// 動作環境: M5Stack Basic / arduino-esp32 core 3.3系 / M5Unified
// ================================================================

#include <M5Unified.h>
#include <SD.h>
#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <time.h>
#include <sys/time.h>
#include "config.h"

// ---- 受信キュー（コールバック内で重い処理をしないための受け渡し箱）----
#define QUEUE_SIZE 8
#define PKT_MAX    256   // ESP-NOWの上限250バイト+終端に収まるサイズ
static char queueBuf[QUEUE_SIZE][PKT_MAX];
static volatile int qHead = 0;  // コールバック(書く側)が進める
static volatile int qTail = 0;  // loop(読む側)が進める

// ---- ノードごとの最新状態（画面表示用）----
struct NodeState {
  bool     seen     = false;   // 一度でも受信したか
  uint32_t lastMs   = 0;       // 最終受信時刻(millis)
  uint32_t seq      = 0;
  float    t        = 0;       // 生値
  float    h        = 0;
  bool     sensorErr = false;
};
static NodeState nodes[NODE_COUNT];

static bool     clockSet  = false;  // TIMEコマンドで時刻設定済みか
static bool     sdOk      = false;
static uint32_t dropCount = 0;      // 解釈できなかった受信の数
static M5Canvas canvas(&M5.Display);
static bool     spriteOk = false;  // Basic(PSRAM無し)ではスプライト確保に失敗し得る
static String   myMac;

// ---- ESP-NOW受信コールバック（コピーだけして即返す）----
void onRecv(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  int next = (qHead + 1) % QUEUE_SIZE;
  if (next == qTail) return;                 // キューが満杯なら捨てる
  if (len <= 0 || len >= PKT_MAX) return;    // 長すぎるものも捨てる
  memcpy(queueBuf[qHead], data, len);
  queueBuf[qHead][len] = '\0';
  qHead = next;
}

// ---- 手組みJSONの読み取りヘルパー（契約のフィールドだけ拾う）----
static bool findU32(const char *json, const char *key, uint32_t &out) {
  char pat[24];
  snprintf(pat, sizeof(pat), "\"%s\":", key);
  const char *p = strstr(json, pat);
  if (!p) return false;
  out = strtoul(p + strlen(pat), nullptr, 10);
  return true;
}
static bool findFloat(const char *json, const char *key, float &out) {
  char pat[24];
  snprintf(pat, sizeof(pat), "\"%s\":", key);
  const char *p = strstr(json, pat);
  if (!p) return false;
  out = strtof(p + strlen(pat), nullptr);
  return true;
}
static bool findStr(const char *json, const char *key, char *out, size_t n) {
  char pat[24];
  snprintf(pat, sizeof(pat), "\"%s\":\"", key);
  const char *p = strstr(json, pat);
  if (!p) return false;
  p += strlen(pat);
  const char *q = strchr(p, '"');
  if (!q || (size_t)(q - p) >= n) return false;
  memcpy(out, p, q - p);
  out[q - p] = '\0';
  return true;
}

static int nodeIndex(const char *id) {
  for (int i = 0; i < NODE_COUNT; i++)
    if (strcmp(id, NODE_IDS[i]) == 0) return i;
  return -1;
}

// ---- 現在時刻を "2026-08-21 10:30:15" 形式で得る ----
static void nowString(char *out, size_t n) {
  time_t tt = time(nullptr);
  struct tm tmv;
  localtime_r(&tt, &tmv);
  strftime(out, n, "%Y-%m-%d %H:%M:%S", &tmv);
}

// ---- SDへ1行追記（openしてすぐclose＝1行ごとflushの契約）----
static void appendLog(const char *line) {
  if (!sdOk) return;
  File f = SD.open(LOG_PATH, FILE_APPEND);
  if (!f) { sdOk = false; return; }
  f.println(line);
  f.close();
}

// ---- 受信1件を処理: 状態更新 + CSV追記 ----
static void handlePacket(const char *json) {
  char id[8] = "";
  uint32_t seq = 0;
  if (!findStr(json, "id", id, sizeof(id)) || !findU32(json, "seq", seq)) {
    dropCount++;
    Serial.printf("drop (no id/seq): %s\n", json);
    return;
  }
  uint32_t v = 0;
  if (!findU32(json, "v", v) || v != SCHEMA_VERSION) {
    dropCount++;
    Serial.printf("drop (schema v%lu): %s\n", (unsigned long)v, json);
    return;
  }
  int idx = nodeIndex(id);
  if (idx < 0) {
    dropCount++;
    Serial.printf("drop (unknown id): %s\n", json);
    return;
  }

  char errbuf[16] = "";
  bool isErr = findStr(json, "err", errbuf, sizeof(errbuf));
  float t = 0, h = 0;
  if (!isErr && (!findFloat(json, "t", t) || !findFloat(json, "h", h))) {
    dropCount++;
    Serial.printf("drop (no t/h): %s\n", json);
    return;
  }

  // 状態更新（画面用）
  nodes[idx].seen      = true;
  nodes[idx].lastMs    = millis();
  nodes[idx].seq       = seq;
  nodes[idx].sensorErr = isErr;
  if (!isErr) { nodes[idx].t = t; nodes[idx].h = h; }

  // CSV追記（契約: recv_time,clock,node_id,seq,temp_c,hum_pct,status）
  char ts[24];
  nowString(ts, sizeof(ts));
  char line[128];
  if (isErr) {
    snprintf(line, sizeof(line), "%s,%s,%s,%lu,,,sensor_err",
             ts, clockSet ? "set" : "unset", id, (unsigned long)seq);
  } else {
    snprintf(line, sizeof(line), "%s,%s,%s,%lu,%.1f,%.1f,ok",
             ts, clockSet ? "set" : "unset", id, (unsigned long)seq, t, h);
  }
  appendLog(line);
  Serial.println(line);
}

// ---- シリアルから "TIME 2026-08-17 09:00:00" を受け付ける ----
static void pollSerialTime() {
  static char buf[48];
  static int  pos = 0;
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      buf[pos] = '\0';
      pos = 0;
      int Y, M, D, hh, mm, ss;
      if (sscanf(buf, "TIME %d-%d-%d %d:%d:%d", &Y, &M, &D, &hh, &mm, &ss) == 6) {
        struct tm tmv = {};
        tmv.tm_year = Y - 1900; tmv.tm_mon = M - 1; tmv.tm_mday = D;
        tmv.tm_hour = hh; tmv.tm_min = mm; tmv.tm_sec = ss;
        struct timeval tv = { mktime(&tmv), 0 };
        settimeofday(&tv, nullptr);
        clockSet = true;
        Serial.println("clock set OK");
      } else if (buf[0] != '\0') {
        Serial.println("usage: TIME 2026-08-17 09:00:00");
      }
    } else if (pos < (int)sizeof(buf) - 1) {
      buf[pos++] = c;
    }
  }
}

// ---- 画面描画（1秒ごと）----
// スプライト(メモリ上の下書き)が確保できればちらつきゼロで描く。
// Basic(PSRAM無し)で確保に失敗したときは画面へ直接描く(多少ちらつくが動く)。
static void drawScreen() {
  lgfx::LovyanGFX &g = spriteOk ? static_cast<lgfx::LovyanGFX &>(canvas)
                                : static_cast<lgfx::LovyanGFX &>(M5.Display);
  g.fillRect(0, 0, 320, 240, TFT_BLACK);
  g.setTextSize(1);

  // ヘッダ: 時刻（未設定なら警告）
  char ts[24];
  nowString(ts, sizeof(ts));
  if (clockSet) {
    g.setTextColor(TFT_WHITE);
    g.setCursor(8, 6);
    g.printf("%s", ts);
  } else {
    g.setTextColor(TFT_RED);
    g.setCursor(8, 6);
    g.printf("JIKOKU MISETTEI  (serial: TIME ...)");
  }
  g.drawFastHLine(0, 22, 320, TFT_DARKGREY);

  // ノード行
  for (int i = 0; i < NODE_COUNT; i++) {
    int y = 34 + i * 44;
    g.setTextColor(TFT_CYAN);
    g.setTextSize(2);
    g.setCursor(8, y);
    g.printf("%s", NODE_IDS[i]);

    if (!nodes[i].seen) {
      g.setTextColor(TFT_DARKGREY);
      g.setCursor(60, y);
      g.printf("---");
    } else if (millis() - nodes[i].lastMs > STALE_MS) {
      g.setTextColor(TFT_RED);
      g.setCursor(60, y);
      g.printf("MUOUTOU %lus", (unsigned long)((millis() - nodes[i].lastMs) / 1000));
    } else if (nodes[i].sensorErr) {
      g.setTextColor(TFT_ORANGE);
      g.setCursor(60, y);
      g.printf("SENSOR ERR");
    } else {
      // 表示にだけ校正オフセットを適用（CSVは生値のまま）
      g.setTextColor(TFT_WHITE);
      g.setCursor(60, y);
      g.printf("%5.1fC %5.1f%%", nodes[i].t + CAL_OFFSET_T[i], nodes[i].h);
      g.setTextSize(1);
      g.setTextColor(TFT_DARKGREY);
      g.setCursor(62, y + 18);
      g.printf("seq=%lu  %lus ago", (unsigned long)nodes[i].seq,
               (unsigned long)((millis() - nodes[i].lastMs) / 1000));
      g.setTextSize(2);
    }
  }

  // フッタ: 自分のMAC（ノードのconfig.hに転記する値）とSD状態
  g.setTextSize(1);
  g.drawFastHLine(0, 214, 320, TFT_DARKGREY);
  g.setTextColor(TFT_GREENYELLOW);
  g.setCursor(8, 222);
  g.printf("MAC %s", myMac.c_str());
  g.setTextColor(sdOk ? TFT_GREEN : TFT_RED);
  g.setCursor(240, 222);
  g.printf(sdOk ? "SD OK" : "SD NG");
  if (dropCount > 0) {
    g.setTextColor(TFT_ORANGE);
    g.setCursor(180, 222);
    g.printf("drop:%lu", (unsigned long)dropCount);
  }

  if (spriteOk) canvas.pushSprite(0, 0);
}

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);
  Serial.begin(115200);

  // 8bitカラーにしてメモリを半分に(320x240で約77KB)。それでも確保できなければ直接描画
  canvas.setColorDepth(8);
  spriteOk = (canvas.createSprite(320, 240) != nullptr);
  if (!spriteOk) Serial.println("sprite確保失敗 -> 直接描画モード");

  // SDカード（M5Stack BasicはCS=GPIO4）
  sdOk = SD.begin(SD_CS_PIN);
  if (sdOk && !SD.exists(LOG_PATH)) {
    File f = SD.open(LOG_PATH, FILE_WRITE);
    if (f) {
      f.println("recv_time,clock,node_id,seq,temp_c,hum_pct,status");
      f.close();
    }
  }

  // ESP-NOW受信の準備
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  esp_wifi_set_channel(WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);
  myMac = WiFi.macAddress();
  Serial.printf("=== onmura gateway ===\nMAC: %s\n", myMac.c_str());
  Serial.println("時刻設定: TIME 2026-08-17 09:00:00 のように送信");

  if (esp_now_init() != ESP_OK) {
    Serial.println("esp_now_init failed. 5秒後に再起動します");
    delay(5000);
    ESP.restart();
  }
  esp_now_register_recv_cb(onRecv);
}

void loop() {
  M5.update();
  pollSerialTime();

  // キューにたまった受信を処理
  while (qTail != qHead) {
    handlePacket(queueBuf[qTail]);
    qTail = (qTail + 1) % QUEUE_SIZE;
  }

  // 1秒ごとに画面更新
  static uint32_t lastDraw = 0;
  if (millis() - lastDraw >= 1000) {
    lastDraw = millis();
    drawScreen();
  }
  delay(10);
}
