// =====================================================================
// 教室の温度ムラ「見える化」プロジェクト — ノードケース
//
// 収納するもの:
//   - ESP32-DevKitC-32E（秋月 115673）… 本体ボックスに収納
//   - AE-SHT31 温湿度センサー（秋月 112125）… 横づけの通風ポッドに収納
//   - 両者はメスメスのジャンパー線4本（3V3/GND/SDA21/SCL22）で接続
//
// 設計方針:
//   ESP32は自己発熱する（無線送信＋レギュレータ）ため、センサーを
//   同じ箱に入れると温度が高めにずれる。そこでセンサーは本体の外側に
//   ルーバー（通風スリット）付きの小さなポッドとして分離し、
//   アリ溝（ダブテール）で本体側面にスライド装着する。
//
// 印刷: Bambu Lab A1 mini / PLA / 0.2mm層 / サポート不要
//   body … そのままの向き（開口部を上）
//   lid  … 天板を下（このファイルの出力そのままの向き）
//   pod  … そのままの向き（開口部を下＝造形の底）
//
// 使い方:
//   下の part を切り替えて1パーツずつSTLに書き出す。
//   コマンドライン例:
//     openscad -D 'part="body"' -o stl/node_case_body.stl node_case.scad
// =====================================================================

part = "all"; // "body" / "lid" / "pod" / "all"（all は配置プレビュー用）

// ---------------------------------------------------------------
// ★ 印刷前にノギスで実測して合わせるパラメータ ★
// ---------------------------------------------------------------
esp_l = 54.4;  // ESP32-DevKitC-32E 基板の長さ
esp_w = 27.9;  // 同 幅
esp_t = 1.6;   // 同 板厚

sht_w = 14.0;  // AE-SHT31 基板の幅（溝にくわえさせる方向。要実測！）
sht_t = 1.2;   // 同 板厚（部品高さぶんの余裕は別途 gap で確保）

tol     = 0.4; // 基板まわりの遊び（片側）。きつい/ゆるい時はここを調整
lid_tol = 0.2; // フタのはめあい。きつければ0.3に
dove_tol= 0.3; // アリ溝のはめあい

// ---------------------------------------------------------------
// 本体ボックスの寸法
// ---------------------------------------------------------------
wall    = 2.0;  // 壁厚
floor_t = 2.0;  // 底厚
bay_h   = 22;   // 基板下の空間（ピン＋ジャンパーコネクタ14mm＋曲げ余裕）
top_h   = 6;    // 基板上の空間（部品高さ＋余裕）

cav_l  = esp_l + 2*tol;
cav_w  = esp_w + 2*tol;
body_l = cav_l + 2*wall;             // ≈59.2
body_w = cav_w + 2*wall;             // ≈32.7
body_h = floor_t + bay_h + esp_t + top_h;  // ≈31.6

ledge_d = 2.5;  // 基板を支える棚（短辺側。ピンの無い端3mm以内に収める）

usb_w   = 13;   // micro-USBプラグの逃がし幅（モールド部が通る幅）
wire_hole_w = 12; // センサー行きジャンパー4本の出口
wire_hole_h = 10;

// アリ溝レール（本体側がオス）
rail_cx   = body_l - 14; // レール中心のX位置（アンテナ側の端寄り）
rail_h    = 27;          // レールの高さ
rail_root = 6;           // 根元幅
rail_tip  = 8.4;         // 先端幅
rail_d    = 2.4;         // 突出量

// ---------------------------------------------------------------
// フタ（かぶせ式キャップ）
// ---------------------------------------------------------------
lid_wall = 1.6;
lid_top  = 2.0;
skirt    = 8.0;   // スカート（側面に下りる部分）の高さ
post     = 4.0;   // 基板おさえポストの太さ
post_gap = 0.3;   // ポスト先端と基板の隙間（押し付けすぎない）

lid_l = body_l + 2*(lid_tol + lid_wall);
lid_w = body_w + 2*(lid_tol + lid_wall);
post_h = top_h - post_gap;

// ---------------------------------------------------------------
// センサーポッド
// ---------------------------------------------------------------
p_wall  = 1.6;
p_back  = 4.5;            // アリ溝側の厚壁
pw_in   = sht_w + 2.0;    // 内寸X（基板幅＋余裕）
pd_in   = 10;             // 内寸Y
p_h     = 30;             // 全高（底は全開放）
p_top   = 2.0;            // 天板厚
rib_d   = (pw_in - (sht_w + 0.5)) / 2; // リブ突出量 → 溝スパン=基板幅+0.5
rib_gap = sht_t + 1.2;    // 基板をくわえる溝の幅（部品ぶんの余裕込み）

pod_x = pw_in + 2*p_wall;
pod_y = pd_in + p_wall + p_back;

// =====================================================================
eps = 0.01;

// ---- 本体 ----------------------------------------------------------
module body() {
    difference() {
        cube([body_l, body_w, body_h]);

        // 内側の空洞（上面開口）
        translate([wall, wall, floor_t])
            cube([cav_l, cav_w, body_h]);

        // micro-USBの切り欠き（x=0の短辺壁、上まで開いたU字ノッチ）
        translate([-eps, body_w/2 - usb_w/2, floor_t + bay_h - 3])
            cube([wall + 2*eps, usb_w, body_h]);

        // センサー行きジャンパー線の出口（y=0の長辺壁、底面レベル）
        // ポッド（幅pod_x）がレール中心に来ても塞がれない位置に置く
        translate([rail_cx - (pw_in + 2*p_wall)/2 - 1.6 - wire_hole_w, -eps, floor_t])
            cube([wire_hole_w, wall + 2*eps, wire_hole_h]);

        // 通気スリット（両長辺壁の上段＝部品まわりの熱を逃がす）
        for (x = [8, 14, 20, 26])
            translate([x, -eps, floor_t + bay_h + 2])
                cube([2, wall + 2*eps, esp_t + top_h - 3]);
        for (x = [8, 14, 20, 26, 32, 38, 44])
            translate([x, body_w - wall - eps, floor_t + bay_h + 2])
                cube([2, wall + 2*eps, esp_t + top_h - 3]);

        // 底面の通気スリット（下から吸気→上へ抜ける）
        for (x = [12, 22, 32, 42])
            translate([x, body_w/2 - 9, -eps])
                cube([2, 18, floor_t + 2*eps]);
    }

    // 基板を支える棚（両短辺。ピンヘッダの無い端部で受ける）
    translate([wall, wall, floor_t])
        cube([ledge_d, cav_w, bay_h]);
    translate([body_l - wall - ledge_d, wall, floor_t])
        cube([ledge_d, cav_w, bay_h]);

    // アリ溝レール（オス、y=0外壁から-y方向へ突出する縦レール）
    // 断面はXY平面の台形（根元6mm→先端8.4mm）をZ方向に押し出す
    translate([rail_cx, 0, 0])
        linear_extrude(rail_h)
            polygon([[-rail_root/2, 0.1], [rail_root/2, 0.1],
                     [rail_tip/2, -rail_d], [-rail_tip/2, -rail_d]]);

    // 取付け耳（反対側の長辺、ネジ・結束バンド・画鋲なんでも用）
    for (x = [4, body_l - 16])
        translate([x, body_w - 0.1, 0])   // 0.1mm壁に食い込ませて一体化する
            difference() {
                cube([12, 8.1, 3]);
                translate([6, 4.6, -eps]) cylinder(h = 3 + 2*eps, d = 4, $fn = 24);
            }
}

// ---- フタ（印刷向き＝天板が下）--------------------------------------
module lid() {
    difference() {
        cube([lid_l, lid_w, lid_top + skirt]);

        // スカート内側（本体外形＋はめあい遊び）
        translate([lid_wall, lid_wall, lid_top])
            cube([lid_l - 2*lid_wall, lid_w - 2*lid_wall, skirt + eps]);

        // 天板の通気スリット
        for (x = [10, 16, 22, 28, 34, 40, 46])
            translate([x, lid_w/2 - 10, -eps])
                cube([2, 20, lid_top + 2*eps]);

        // 両短辺スカートの切り欠き（USBの逃がし兼、フタを外す指がかり）
        for (sx = [-eps, lid_l - lid_wall - eps])
            translate([sx, lid_w/2 - (usb_w + 2)/2, lid_top])
                cube([lid_wall + 2*eps, usb_w + 2, skirt + 2*eps]);
    }

    // 基板おさえポスト（棚の真上に軽く効かせる）
    off = lid_wall + lid_tol;   // 本体座標→フタ座標のオフセット
    for (bx = [wall + ledge_d/2, body_l - wall - ledge_d/2])
        translate([off + bx - post/2, off + body_w/2 - post/2, lid_top])
            cube([post, post, post_h]);
}

// ---- センサーポッド --------------------------------------------------
module pod() {
    difference() {
        cube([pod_x, pod_y, p_h]);

        // 空洞（底面は全開放＝空気の入口＋配線の通り道）
        translate([p_wall, p_wall, -eps])
            cube([pw_in, pd_in, p_h - p_top + eps]);

        // ルーバー（前面）
        for (z = [5, 10, 15, 20])
            translate([p_wall + 1, -eps, z])
                cube([pw_in - 2, p_wall + 2*eps, 2.5]);

        // ルーバー（両側面）
        for (z = [5, 10, 15, 20], sx = [-eps, pod_x - p_wall - eps])
            translate([sx, p_wall + 1.5, z])
                cube([p_wall + 2*eps, pd_in - 3, 2.5]);

        // アリ溝（メス、背面の厚壁 y=pod_y の面から内側へ。
        // 下から差し込み、溝の上端がレール上端に乗って止まる）
        translate([pod_x/2, pod_y, -eps])
            linear_extrude(rail_h + 0.5)
                polygon([[-rail_root/2 - dove_tol, 0.1],
                         [ rail_root/2 + dove_tol, 0.1],
                         [ rail_tip/2 + dove_tol, -(rail_d + 0.15)],
                         [-rail_tip/2 - dove_tol, -(rail_d + 0.15)]]);
    }

    // 基板をくわえる縦リブ（左右の内壁に2本ずつ→溝を形成。下から挿入）
    rib_y0 = p_wall + pd_in/2 - rib_gap/2 - 2;  // 手前側リブ
    rib_y1 = p_wall + pd_in/2 + rib_gap/2;      // 奥側リブ
    for (sx = [p_wall, pod_x - p_wall - rib_d], ry = [rib_y0, rib_y1])
        translate([sx == p_wall ? p_wall : pod_x - p_wall - rib_d, ry, 0])
            cube([rib_d, 2, p_h - p_top]);
}

// ---- 出力 -----------------------------------------------------------
if (part == "body") body();
if (part == "lid")  lid();
if (part == "pod")  pod();
if (part == "all") {
    body();
    translate([0, body_w + 25, 0]) lid();
    translate([body_l + 15, 0, 0]) pod();
}
