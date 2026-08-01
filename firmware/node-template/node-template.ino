// ================================================================
// 教室の温度ムラ「見える化」 ノード側テンプレート
//
// 役割: SHT31で温湿度を測り、30秒ごとにJSONをESP-NOWで
//       集約M5Stackへ送る。データ契約v1（docs/data-contract.md）準拠。
//
// 各メンバーはこのフォルダを firmware/nodes/n1 などにコピーして
// 自分のノードとして育てる。書き換えてよいのは:
//   - config.h の NODE_ID と GATEWAY_MAC
//   - readSensor() の中身（別センサーに差し替える場合）
// 送信部・JSON部は「契約」なので変更しない（変えたいときは合意→v+1）。
//
// 動作環境: ESP32-DevKitC-32E / arduino-esp32 core 3.3系
// ================================================================

#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <Wire.h>
#include "config.h"

static uint32_t seq = 0;              // 通番（起動から+1ずつ。欠落検出用）
static volatile bool sendDone = false; // 送信コールバックが来たか
static volatile bool sendOk   = false; // 送達確認の結果

// ---- 送信結果コールバック（ESP-NOWが送達確認を返してくる）----
void onSent(const wifi_tx_info_t *info, esp_now_send_status_t status) {
  sendOk   = (status == ESP_NOW_SEND_SUCCESS);
  sendDone = true;
}

// ---- SHT31 CRC-8チェック（多項式0x31, 初期値0xFF）----
static uint8_t sht31Crc(const uint8_t *data, int len) {
  uint8_t crc = 0xFF;
  for (int i = 0; i < len; i++) {
    crc ^= data[i];
    for (int b = 0; b < 8; b++) {
      crc = (crc & 0x80) ? (uint8_t)((crc << 1) ^ 0x31) : (uint8_t)(crc << 1);
    }
  }
  return crc;
}

// ---- センサー読み取り（ここが各自の担当部分）----
// 成功: tempC/humPct に値を入れて true を返す
// 失敗: false を返す（呼び出し側が err 送信に切り替える）
bool readSensor(float &tempC, float &humPct) {
  // 単発測定コマンド 0x2400（高リピータビリティ・クロックストレッチなし）
  Wire.beginTransmission(SHT31_ADDR);
  Wire.write(0x24);
  Wire.write(0x00);
  if (Wire.endTransmission() != 0) return false;

  delay(20);  // 測定待ち（データシート上は最大15ms）

  uint8_t buf[6];
  if (Wire.requestFrom((int)SHT31_ADDR, 6) != 6) return false;
  for (int i = 0; i < 6; i++) buf[i] = Wire.read();

  // buf: [温度H][温度L][CRC][湿度H][湿度L][CRC]
  if (sht31Crc(buf, 2) != buf[2]) return false;
  if (sht31Crc(buf + 3, 2) != buf[5]) return false;

  uint16_t rawT = ((uint16_t)buf[0] << 8) | buf[1];
  uint16_t rawH = ((uint16_t)buf[3] << 8) | buf[4];
  tempC  = -45.0f + 175.0f * rawT / 65535.0f;
  humPct = 100.0f * rawH / 65535.0f;
  return true;
}

// ---- 1回送信して送達確認を待つ。true=届いた ----
static bool sendOnce(const char *json) {
  sendDone = false;
  sendOk   = false;
  esp_err_t e = esp_now_send(GATEWAY_MAC, (const uint8_t *)json, strlen(json));
  if (e != ESP_OK) return false;
  uint32_t t0 = millis();
  while (!sendDone && millis() - t0 < 300) delay(1);  // 送達確認を最大300ms待つ
  return sendDone && sendOk;
}

// ---- 契約どおりの送信: 失敗したら1秒後に1回だけ再送 ----
static void sendWithRetry(const char *json) {
  if (sendOnce(json)) {
    Serial.printf("send ok : %s\n", json);
    return;
  }
  delay(1000);
  if (sendOnce(json)) {
    Serial.printf("send ok (retry): %s\n", json);
  } else {
    Serial.printf("send FAIL: %s\n", json);  // 諦めて次の周期に任せる（契約）
  }
}

void setup() {
  Serial.begin(115200);
  delay(300);
  Serial.println();
  Serial.println("=== onmura node ===");
  Serial.printf("NODE_ID=%s  schema v%d\n", NODE_ID, SCHEMA_VERSION);

  Wire.begin(PIN_SDA, PIN_SCL);

  // ESP-NOWはWiFi(STA)の上で動く。APには接続しない
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  esp_wifi_set_channel(WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);
  Serial.print("my MAC: ");
  Serial.println(WiFi.macAddress());

  // ありがちな設定忘れを起動時に警告（GATEWAY_MACが初期値のまま）
  bool macZero = true;
  for (int i = 0; i < 6; i++) if (GATEWAY_MAC[i] != 0) macZero = false;
  if (macZero) {
    Serial.println("!!! 警告: GATEWAY_MAC が未設定(全て0x00)です。");
    Serial.println("!!! M5Stackの画面に出るMACを config.h に転記してください。");
  }

  if (esp_now_init() != ESP_OK) {
    Serial.println("esp_now_init failed. 5秒後に再起動します");
    delay(5000);
    ESP.restart();
  }
  esp_now_register_send_cb(onSent);

  // 宛先（集約M5Stack）をピア登録
  esp_now_peer_info_t peer = {};
  memcpy(peer.peer_addr, GATEWAY_MAC, 6);
  peer.channel = WIFI_CHANNEL;
  peer.encrypt = false;  // 契約: 暗号化なし（環境データのみ・単純さ優先）
  if (esp_now_add_peer(&peer) != ESP_OK) {
    Serial.println("add_peer failed. config.h の GATEWAY_MAC を確認してください");
  }
}

void loop() {
  char json[128];
  float t, h;

  if (readSensor(t, h)) {
    // 正常時: {"v":1,"id":"n1","seq":123,"t":26.4,"h":55.2}
    snprintf(json, sizeof(json),
             "{\"v\":%d,\"id\":\"%s\",\"seq\":%lu,\"t\":%.1f,\"h\":%.1f}",
             SCHEMA_VERSION, NODE_ID, (unsigned long)seq, t, h);
  } else {
    // 読み取り失敗時: t/h を省略して err を送る（生存報告を兼ねる）
    snprintf(json, sizeof(json),
             "{\"v\":%d,\"id\":\"%s\",\"seq\":%lu,\"err\":\"sensor\"}",
             SCHEMA_VERSION, NODE_ID, (unsigned long)seq);
  }
  seq++;

  sendWithRetry(json);
  delay(SEND_INTERVAL_MS);  // 30秒待って次の測定へ
}
