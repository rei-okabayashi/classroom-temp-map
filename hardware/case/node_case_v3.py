"""センサーノードケース v3 — 組立可能性の回復版（全高58.5・3部品）

v2.2からの変更（§8-4。レイ承認済み: chassis廃止=OK / box磁石shell2個後退=OK）:
  - ③ 基板棚はY±10の中央帯のみ（ピン列Y±12.68・ハウジング包絡±10.98〜14.38を逃がす）
  - ④ センサーは上から落とし込み（クレードル: 後席2+タブ先席1の3点着座、
      Y±7.15フランク壁+保持ナブ、-Xストップピラー、+Xエンドストップ）
  - ② chassis廃止。boxはパラペット内壁のコルベル4個（上面24.5・張り出し1.5）に着座。
      boxのスパイン受けカラー+床スロットも削除（スパイン消滅のため）
  - ① ビードを滑らか半円カプセル（R0.8・突出0.55）に置換＋箱壁に受け溝（R0.95・深0.45）新設
      ＋箱上縁リード面取り1.2＋カラー段の余裕0.3→0.6（COLLAR_TOP 24.0→23.7）
  - 磁石はshell2個のみ（boxの磁石+ボスは削除。壁予算2.22<磁石厚2.4で成立疑いのため）
  - boxプリンスリングを低くする（ハウジング包絡の下端3.6と衝突するため）
  - 外装（パラペット入れ子・V溝・カラー帯面一・全高58.5）はv2.2のまま=レイ承認済みの見た目

2026-08-29夕 クーポン実印刷の失敗（微細部）を受けた印刷性是正（design-rules.md
「最小フィーチャ寸法」新設と対。数値の正本は本文パラメータ）:
  - ナブ張り出し0.3/0.15→0.5+リード（幅1.0〜2.0・高さ3層+1層）
  - フランク壁1.6・タブ脇壁1.2x1.6・-Xストップ壁1.6、いずれも水平リブで隣接構造に
    接続して孤立柱をやめる（PLA Matteの層間強度はBasicの43%・TDS実測）
  - サドルガイド張り出し0.38→0.48（遊び0.8→0.6。verify_assemblyの包絡も±0.3に連動）
  - 磁石ポケット2個→スタジアムスロット1本（間に残る0.6mmフィンを排除）
  - ビードR1.0/突出0.6・受け溝R1.15/深0.5（食い込み0.35）
  - 接地面取りは外周のみ（細い床ストリップの第1層痩せ対策）・刻印を太字化

2026-08-30 フル初回印刷のレイ所見4点による改修:
  ① センサー先端ツメ新設（張り出し1.0=チーク2枚+ブリッジ天井のトンネル。挿入は
     「タブを先に差し込み→後端を落とす」に変更、傾け挿入ゲートで検証）＋フランクナブ
     食い込み0.15→0.20/側。※両側ナブの素直な1.0mm化は通過隙間12.7<基板幅14.0で
     挿入不能のため不採用（先端ツメが浮き上がりの真因対策）
  ② shell-boxスナップ新設: boxネック外面(Y±)ビード4本（台座0.25+ノーズR0.6）+
     パラペット内面の受け溝R0.95深0.5（ギャップ0.5を跨いで食い込み0.30・スラック0.2・上唇0.35）
  ③ lid放熱: 押さえパッドを煙突化(壁1.2・CPU直上貫通)+プレートにφ3.2ハニカム孔
     ／box左壁の排気スリットを下へ延長(z14.5→10.0)して給気入口を拡大
  ④ box床の前寄り給気スロット2本を閉鎖（レイ指示。給気は壁スリット+配線穴が担う）
  ⑤ 磁石をスタジアムスロット(±7共有)→独立円ポケット2個(±19.5・縁間25.6mm)へ
     （磁石どうしが引き寄せ合って設置できない対策。SHT31への磁気影響は調査済み=無し）
  ⑦ boxネック帯の薄壁統合（レイ所見「外壁と内壁が細すぎて不安定になりそう」）:
     ネック帯z2..4.1はフレア裏のくさび壁(0→2mm)+0.1隙間+プリンスリング1.9の
     薄壁2枚が非接合で並ぶ構造だった → プリンスリングを廃止し段付きキャビティ
     （下帯z2..3.4を一回り小さく掘る）で一体の2.5〜3.7mm壁に統合。外形は不変
  ⑧ lidハニカム孔を押さえ筒のある側(X-)のみに限定（レイ指示: ESP32の赤LEDが
     CPUと反対側(X+)に来て眩しい→LED側は無孔の目隠しに）。格子・筒・嵌合は不変で
     孔のカット対象だけ x<0 のセルに絞る（48孔→23孔。CPU直上ベントは全数維持）
  ⑨ 壁マウント対応: 長辺(Y±)の側面を本体33.5と面一化（レイ所見「横のでっぱりが
     邪魔で壁にくっつき切らない」）。lidのY側スカートを廃止し、スカートは短辺(X±)の
     脚2対のみ・ビード係合もX±壁へ移設（Y位置決めは箱内壁に沿う下垂フィン2枚）。
     カラー帯はX±のウィングパッド2枚に置換。背面(Y+)はshell〜lidまで単一平面になり
     磁石面が壁へ密着する。X±の張り出し1.85/側・全高58.5・ビード断面は不変

部品: shell_n1..n4（外殻+センサークレードル・刻印つき）/ box / lid
組立位置(ワールドZ): shell 0 / box +24.5 / lid +48.8。全高58.5。
座標系: 各部品 XY中心原点・Z0=部品底面。前=Y- / 背面(机側)=Y+ / USB=X+。
検証: validate_stl + check_floating + verify_assembly.py --target v3（§8-5ゲート）
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
OUT = os.path.dirname(os.path.abspath(__file__))

from build123d import (
    Align, Axis, Box, Cylinder, GeomType, Plane, Pos, RegularPolygon, Sphere,
    chamfer, extrude, fillet, export_stl,
)

# ============================================================
# 共通パラメータ
# ============================================================
WALL = 2.0
FOOT_X, FOOT_Y = 60.3, 33.5
CORNER_R = 3.0
IN_X, IN_Y = FOOT_X - 2 * WALL, FOOT_Y - 2 * WALL   # 56.3 x 29.5

BASE_H = 19.5              # 旧moat床の名残り高さ（パラペット形状の基準に使用）
GAP = 5.0                  # 空気断絶帯（要件R1。BASE_H+GAP=24.5がboxネック底面）

# 磁石ポケット（ダイソー 超強力ネオジム 13mm・4個入=サンノート。パッケージ実測 φ13.0×厚2.4）
# v3配置: shell背面2個(±7, z9.5) のみ。box磁石は壁予算不足(2.22mm<2.4)で削除（§8-4）
MAGNET_D = 13.0
MAGNET_T = 2.4

# --- box ---
BOX_H = 32.0
BOX_FLOOR = 2.0
NECK_INSET = 2.0           # 裾の絞り量（パラペットに入る）
NECK_H = 2.0               # ネック高さ（この上に45°フレア）
SHELF_Z = 21.0             # v3監査是正: 20→21。棚下クリアランス=21-2=19.0にして
                           # §5(c)「ハウジング装着で基板下約17、余裕を見て19〜20確保」の下限を満たす
SHELF_HALF_Y = 10.0        # v3: 棚はY±10の中央帯のみ（§8-4③）
BOARD_T = 1.8
BOARD_ENV_X = 55.3
BOARD_W = 27.94
SADDLE_W = 5.0
SADDLE_X = BOARD_ENV_X / 2 - 4.0 - SADDLE_W / 2
SADDLE_GUIDE_H = 6.0
USB_SLOT_W = 12.0          # レイ指摘(2026-08-29): 13は大きすぎ→microB規格最大10.6+0.7/側=12
                           # （§5(d)の設計基準「規格最大ベース12x9.5」に一致）
USB_SLOT_Z0, USB_SLOT_Z1 = 19.2, 29.0   # プラグ包絡19.9..28.4に余裕0.7/0.6。上は45°ゲーブルで
                                        # 7mmまで絞り天井で閉じる=リムを切らない（旧: リム貫通切妻）
WIRE_HOLE = (12.0, 8.0)
THROAT_XY = (-7.0, 0.0)
STEP_TOP = 3.4             # 段付きキャビティの段上面（2026-08-30⑦: 旧プリンスリング上端を継承）。
                           # v2.2の4.5はハウジング包絡の下端3.6と衝突143mm3（ゲート実測）
                           # → 0.2の余裕を残して3.4。段上面はこれを超えないこと
STEP_T = 2.5               # 下帯z2..3.4の壁厚（上段キャビティ面からの追加肉。ネック面まで一体）
COLLAR_H = 10.0
RIM_CHAMFER = 0.8          # v3: 箱上縁リード面取り（§8-4①）。⑨で1.2→0.8: Y面一化により
                           # リム面取りがプレート直下の露出継ぎ目になるため控えめに。
                           # 角丸ループはchamferが全周伝播するので方向別の差し掛けは不可（実測）

# --- shell-box スナップ（2026-08-30②: 押し込んで嵌る接続。lid-boxのビード/溝と同系） ---
# ネック外面(±14.75)とパラペット内面(±15.25)の面間ギャップ0.5を跨ぐため、ビードは
# 「台座0.25（パラペットに触れない）+ノーズR0.6（軸を台座面に0.05埋め）」の2段構造で
# 先端15.55=パラペット面へ食い込み0.30。軸をネック面上に直置きすると円筒の上下接線が
# 壁面と接線接触して非多様体化する（実測・lesson-tangent-boolean-nonmanifold）。
# X位置はコルベル(X10..18)の外に出す（溝カプセルの球端がコルベル上面24.5を0.05かすめて
# 開エッジになる実測）。軸高さboxローカル0.9→溝はワールド25.4・上唇0.35
SB_BEAD_R = 0.6            # ノーズ半径（軸y=ネック面+0.20・先端+0.80=15.55）
SB_BEAD_Z = 0.9
SB_BEAD_XC = 22.6
SB_BEAD_LEN = 6.0
SB_GROOVE_R = 0.95
SB_GROOVE_DEPTH = 0.5

# --- lid / カラー帯 ---
# 2026-08-30⑨: 長辺(Y±)は面一化。lidは「本体と同輪郭60.3x33.5の板 + X±の端タブ(64.0)
# + X±スカート脚 + Y位置決めフィン」の構成になり、Y側スカート・全周カラー帯は廃止
LID_CLR = 0.25
SKIRT_T = 1.6
SKIRT_ENGAGE = 7.7
LID_PLATE = 2.0
WING = LID_CLR + SKIRT_T                       # 1.85（X±のみの張り出し・タブ/パッド/脚外面=±32.0）
LID_OUT_X = FOOT_X + 2 * WING                  # 64.0
LID_OUT_Y = FOOT_Y                             # 33.5（⑨: 長辺は本体と面一）
BEAD_R = 1.0               # v3: 滑らか半円ビード（積層Box近似の禁止・§8-4①）
BEAD_PROUD = 0.6           # スカート内面からの突出。0.55は1ライン級で輪郭が甘い→0.6へ
                           # （最小フィーチャ規則: 機能係合の張り出し0.5以上）。食い込み=0.6-0.25=0.35
BEAD_LEN = 4.0             # ⑨: 12→4（X±脚の上に収める。球端込み全長6.0・総係合長56→24mm
                           #  =嵌合は軽くなる想定。断面と食い込み0.35は実証済み値のまま）
BEAD_YC = 10.4             # ビード中心のY位置（包絡Y7.4..13.4=脚7.0..13.6の内側に0.4/0.2マージン）
BEAD_Z_LID = 1.5           # ビード軸のlidローカル高さ（v2.2帯0.5..2.45の中心を踏襲）
GROOVE_R = 1.15            # 箱壁の受け溝（半径クリアランス0.15・深さ0.5で緩着座・肩0.35）
GROOVE_DEPTH = 0.5
LEG_HALF_SPAN = 13.6       # スカート脚/端タブ/ウィングパッドの半幅（本体角丸開始13.75の0.15内側）
LEG_CUT_HALF = 7.0         # 脚の中央切欠き半幅（X+はUSBプラグ±6+0.7逃げ・X-は指掛かり。対称）
LEG_CUT_H = 5.2            # 切欠き高さ(lidローカル)。上端=box局所29.5はプラグ包絡28.4+1.1
                           # （旧SKIRT_ENDの端部開放cut_h=5.2と同値を継承）
FIN_LEN = 16.0             # ⑨: Y方向位置決めフィン（Y側スカート廃止の代替・Y±1枚ずつ）
FIN_T = 1.2
FIN_CLR = 0.30             # フィン外面±14.45=箱内壁14.75-0.30（X脚のclr0.25より緩くして
                           #  印刷公差でフィンが先に噛まないようにする・advisor裁定）
FIN_DROP = 2.3             # プレート下面からの下垂。先端box局所29.7はピン上端25.8/
                           #  モジュール上面25.9より3.8上（lid→devkitcゲートで検証）
# 押さえ+放熱ハニカム（2026-08-30③改2: レイ指摘=孔は規則的な六角形・左右均等、
# 押さえはハニカムセルをそのまま下へ伸ばした六角筒）。セル中心間5.6・孔の対辺4.0
# （ウェブ1.6）・筒の外形=セル境界六角形5.6（壁0.8・リム接触13.3mm2）
HEX_PITCH = 5.6
HEX_HOLE_F = 4.0           # 孔の対辺距離
PRESS_PAD_XC = (-19.6, -8.4)   # 押さえ筒にするセル（行y=0・モジュール缶X-27.65..-2.15上）
PRESS_GAP = 0.2
MODULE_TOP = SHELF_Z + BOARD_T + 3.1
COLLAR_TOP = 23.7          # v3: 24.0→23.7（スカート先端24.3との余裕0.3→0.6・§8-4①）
COLLAR_RISE = (LID_OUT_X - FOOT_X) / 2         # 1.85（45°フレアの立ち上がり）

# --- shell ---
PARA_T = 1.5               # パラペット肉厚
PARA_IN_X = FOOT_X - 2 * PARA_T                # 57.3
PARA_IN_Y = FOOT_Y - 2 * PARA_T                # 30.5
PARA_TOP = (BASE_H + GAP) + NECK_H + ((PARA_IN_X - 0.6) - (FOOT_X - 2 * NECK_INSET)) / 2  # 26.7
RING_W = 4.0
RING_T = 2.5
SLIT_W = 2.2
CORBEL_TOP = 24.5          # v3: box受けコルベル上面（=boxネック底面のワールド高さ・§8-4②）
CORBEL_PROT = 2.0          # 張り出し（パラペット内面15.25→13.25。ネック縁14.75を1.5受け、
                           # box底面取り0.5を差し引いてもフラット接触1.0を確保。監査是正）
# SHT31 クレードル（上から落とし込み・§8-4④）
#   ハウジング包絡(X-2.5..12.6, Y±6.5, Z3.5..6.3)と縦脚(X11.3..13.7)の降下コラムを
#   避けて配置する。座標は verify_assembly.py の sht31_phantom() と対で管理。
SHT_SEAT_Z = 7.9           # 基板下面（素子面）
SHT_T = 1.2
SHT_BASE_X0, SHT_BASE_X1 = 10.0, 16.0
SHT_TAB_X1 = 22.0
FLANK_Y0, FLANK_Y1 = 7.35, 8.95    # フランク壁（基板±7.0に対しガイド0.35/側・肉厚1.6=係合壁の下限。
                                   # クーポン実測でMatteの層間脆弱が確定→1.2から増厚しリブで後席に接続）
FLANK_X0, FLANK_X1 = 13.6, 16.2
NUB_TIP_Y = 6.85           # ナブ先端（張り出し0.5=最小フィーチャ規則・基板縁7.0へ0.15/側のクリック）
CRADLE_TOP = 10.2          # 壁・ピラー上端（基板上面9.1+1.1）

NODE_IDS = ["n1", "n2", "n3", "n4"]


# ============================================================
# ヘルパー
# ============================================================
def rounded_prism(x, y, z0, z1, r=CORNER_R):
    p = Pos(0, 0, z0) * Box(x, y, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return fillet(p.edges().filter_by(Axis.Z), radius=r)


def cbox(x, y, z0, z1, cx=0.0, cy=0.0):
    return Pos(cx, cy, z0) * Box(x, y, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN))


def capsule_x(cx, cy, cz, r, length):
    """X軸方向のカプセル（円柱+両端半球）。滑らかなビード/受け溝用（§8-4①）。"""
    cyl = Plane(origin=(cx, cy, cz), z_dir=(1, 0, 0)) * Cylinder(
        r, length, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    return cyl + Pos(cx - length / 2, cy, cz) * Sphere(r) + Pos(cx + length / 2, cy, cz) * Sphere(r)


def capsule_y(cx, cy, cz, r, length):
    """Y軸方向のカプセル（⑨: X±壁のビード/受け溝用）。"""
    cyl = Plane(origin=(cx, cy, cz), z_dir=(0, 1, 0)) * Cylinder(
        r, length, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    return cyl + Pos(cx, cy - length / 2, cz) * Sphere(r) + Pos(cx, cy + length / 2, cz) * Sphere(r)


def stack_taper(width, z_flat, cx, cy, depth, step=0.5):
    """z_flat から45°で幅が閉じる切妻ボリューム（工具用）。"""
    out = None
    w, z = width, z_flat - 0.5
    while w > 0.8:
        layer = cbox(depth, w, z, z + step + 0.2, cx, cy)
        out = layer if out is None else out + layer
        w -= 2 * step
        z += step
    return out


def chamfer_bottom(part, length=0.5, outer_only=False):
    """接地エッジの面取り（エレファントフット対策）。OCCが失敗したら長さを落として再試行。
    outer_only=True は外周フットプリントの縁だけに掛ける: 幅2.5未満の接地フィーチャ
    （クレードル床ストリップ等）に0.5面取りを掛けると第1層が線幅未満に痩せて
    糸になる（2026-08-29クーポン実測）ため、細物を持つ部品では必須。"""
    edges = part.edges().group_by(Axis.Z)[0]
    if outer_only:
        def _is_outer(e):
            b = e.bounding_box()
            return (max(abs(b.max.X), abs(b.min.X)) > FOOT_X / 2 - 0.7
                    or max(abs(b.max.Y), abs(b.min.Y)) > 16.5)
        edges = [e for e in edges if _is_outer(e)]
    for ln in (length, 0.4, 0.3):
        try:
            return chamfer(edges, length=ln)
        except ValueError:
            continue
    long_edges = [e for e in edges if e.length > 15]
    for ln in (length, 0.3):
        try:
            return chamfer(long_edges, length=ln)
        except ValueError:
            continue
    print("[warn] chamfer_bottom失敗: 面取りなしで続行（スライサーのelephant foot補正で代替）")
    return part


def magnet_pocket(part, cx, zc, clr=0.2, skin=0.8, boss_zmax=None):
    """背面壁(Y+)に φ13x2.4 ネオジム1個用の**独立円ポケット**を彫る。
    2026-08-30⑤レイ指摘: 中心±7のスタジアムスロット共有だと磁石どうしが引き寄せ合い
    設置できない→がっつり離した位置(±19.5=縁間25.6mm)に1個ずつ。各磁石は自分のボアに
    捕まるので挿入時に動かない（CA接着は継続）。独立ポケットどうしを近接させると間に
    印刷不能フィンが残る（v2.2実測）が、39mm離れているので無関係。
    センサー真横になるが、SHT31は容量式+バンドギャップのCMOSで静磁場と結合する素子が
    無く、Sensirion公式データシートにも磁気関連の記載・注意は皆無（2026-08-30調査）。
    外皮 skin を残し、壁厚2.0で足りない分は内側ボス(角柱)を足す。開口は室内側。"""
    r = (MAGNET_D + 2 * clr) / 2
    depth = MAGNET_T + clr
    boss_d = depth + skin - WALL                      # 内側に足す厚み
    inner_y = IN_Y / 2
    if boss_d > 0:
        z_hi = zc + r + 1.2 if boss_zmax is None else min(zc + r + 1.2, boss_zmax)
        part += cbox(2 * r + 3.0, boss_d + 1.0, zc - r - 1.2, z_hi,
                     cx, inner_y + 1.0 - (boss_d + 1.0) / 2)
    mouth_y = inner_y - boss_d                        # ポケット開口面
    part -= Plane(origin=(cx, mouth_y - 0.01, zc), z_dir=(0, 1, 0)) * Cylinder(
        r, depth + 0.01, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return part


# ============================================================
# box（ESP32室・裾ネック＋カラー帯つき・v3）
# ============================================================
def build_box():
    # 外殻: ネック(0..3) + 本体(2..32 底縁45°チャンファ=フレア) + カラー帯(bottom..23.7 底縁45°)
    neck = rounded_prism(FOOT_X - 2 * NECK_INSET, FOOT_Y - 2 * NECK_INSET, 0, NECK_H + 1, r=1.5)
    body = rounded_prism(FOOT_X, FOOT_Y, NECK_H, BOX_H)
    body = chamfer(body.edges().group_by(Axis.Z)[0], length=NECK_INSET + 0.1)
    part = body + neck

    # カラー帯 → ⑨でX±の「ウィングパッド」2枚に置換（Y面一のためY側の帯は消滅。
    # X面はlidの端タブ64.0と面一で連なる従来の見た目を維持）。壁に0.5食い込ませて
    # union し、下端3辺は45°フレア（面取り失敗時は段階的に縮めて続行）
    pad_z0 = COLLAR_TOP - COLLAR_RISE - 1.7                       # 20.15
    for sx in (-1, +1):
        pad = cbox(WING + 0.5, 2 * LEG_HALF_SPAN, pad_z0, COLLAR_TOP,
                   sx * (FOOT_X / 2 - 0.5 + (WING + 0.5) / 2))    # X29.65..32.0
        # 底面3辺（外側+両端）だけ面取り。壁内に埋まる内側辺は除外
        # （2.35幅の底面に1.9x2は幾何的に干渉して必ず失敗するため）
        bot = [e for e in pad.edges().group_by(Axis.Z)[0]
               if not (abs(e.bounding_box().min.X) < FOOT_X / 2 - 0.3
                       and abs(e.bounding_box().max.X) < FOOT_X / 2 - 0.3)]
        for ln in (COLLAR_RISE + 0.05, 1.5, 1.0):
            try:
                pad = chamfer(bot, length=ln)
                break
            except ValueError:
                continue
        else:
            print("[warn] ウィングパッドの45°フレア面取り失敗: 垂直のまま続行（下面が張り出す）")
        part += pad

    # 内室（2026-08-30⑦: 段付き2段掘り。下帯z2..3.4は一回り小さく掘り、ネック帯の
    # 「フレア裏くさび壁0→2mm + 0.1隙間 + プリンスリング1.9」の薄壁2枚を
    # 一体の2.5〜3.7mm壁に統合する。段上面3.4=ハウジング包絡下端3.6-0.2は不変条件）
    cavity = cbox(IN_X, IN_Y, STEP_TOP, BOX_H + 1)
    cavity = fillet(cavity.edges().filter_by(Axis.Z), radius=1.5)
    part -= cavity
    lower_cav = cbox(IN_X - 2 * STEP_T, IN_Y - 2 * STEP_T, BOX_FLOOR, STEP_TOP + 0.5)
    lower_cav = fillet(lower_cav.edges().filter_by(Axis.Z), radius=1.5)
    part -= lower_cav       # 上端は3.9まで食い込ませ同一平面フェイスを避ける（上段が既に空洞）

    # 上縁リード面取り（⑨: 全周0.8均一。当初のX±1.2/Y±0.4の2段掛けは、角丸矩形の
    # 上縁ループがG1連続=OCCのchamferが指定1辺からループ全周へ伝播するため原理的に不可
    # （実測: X2辺指定でY縁も15.55まで削れた）→ advisor事前裁定のフォールバック値0.8を
    # 正式採用。X側は0.8+ビード自己リードで挿入でき、Y側は面一プレート下の影線になる）
    outer_top = [e for e in part.edges().group_by(Axis.Z)[-1]
                 if (abs(e.bounding_box().max.X) > FOOT_X / 2 - 0.6
                     or abs(e.bounding_box().min.X) > FOOT_X / 2 - 0.6
                     or abs(e.bounding_box().max.Y) > FOOT_Y / 2 - 0.6
                     or abs(e.bounding_box().min.Y) > FOOT_Y / 2 - 0.6)]
    for ln in (RIM_CHAMFER, 0.6):
        try:
            part = chamfer(outer_top, length=ln)
            break
        except ValueError:
            continue
    else:
        print("[warn] 上縁リード面取り失敗: 面取りなしで続行（要目視確認）")

    # （2026-08-30⑦: 内側プリンスリングは段付きキャビティへの統合に伴い削除）

    # サドル（基板の棚・§8-4③: 支持はY±10の中央帯のみ。柱ごと絞る）
    # ガイド壁（Y±14.37で基板を案内）はv2.2のまま維持
    # ガイドの張り出しは壁面14.75-ガイド面。遊び0.8では張り出し0.38=1ライン未満で
    # 輪郭が出ない（クーポン実測「ガイド周り」失敗）→遊び0.6にして張り出し0.48を確保
    guide_span = BOARD_W + 0.6
    for sx in (-1, +1):
        cx = sx * SADDLE_X
        part += cbox(SADDLE_W, 2 * SHELF_HALF_Y, BOX_FLOOR - 1, SHELF_Z, cx)
        guide = cbox(SADDLE_W, guide_span + 1.8, SHELF_Z - 1, SHELF_Z + SADDLE_GUIDE_H, cx)
        guide -= cbox(SADDLE_W + 2, guide_span, SHELF_Z - 2, SHELF_Z + SADDLE_GUIDE_H + 1, cx)
        part += guide

    # （v3: スパイン受けカラー+床スロットは chassis廃止に伴い削除）

    # 床: 配線穴のみ（前寄り給気スロット2本は2026-08-30④レイ指示で閉鎖。
    # 給気は左壁スリット（下へ延長済み）+配線穴が担う）
    part -= cbox(WIRE_HOLE[0], WIRE_HOLE[1], -1, BOX_FLOOR + 1, THROAT_XY[0], THROAT_XY[1])

    # USBポート（右壁 12x9.8）。上部は45°段付きゲーブルで幅8まで絞り、0.8厚(4層)の天井で
    # 閉じる（ブリッジ8mm=許容帯・リム全周が繋がる）。蓋スカートの端部開放(29.5..32)が
    # 外側を覆うので、ケーブルはポートから下へ抜ける
    wall_cx = IN_X / 2 + 2.0
    part -= cbox(8.0, USB_SLOT_W, USB_SLOT_Z0, USB_SLOT_Z1, wall_cx)
    w, z = USB_SLOT_W, USB_SLOT_Z1
    while w > 8.0:
        w -= 1.0
        part -= cbox(8.0, w, z, z + 0.7, wall_cx)
        z += 0.5

    # 排気スリット: 左壁(X-)・フレアの下の帯（背面=磁石面は無地）
    # 2026-08-30③: lid放熱孔の新設で本スリットは給気入口を兼ねる→下へ延長(14.5→10.0)
    left_cx = -(IN_X / 2 + 2.0)
    for cy in (-9.0, -3.0, 3.0, 9.0):
        part -= cbox(8.0, SLIT_W, 10.0, 20.4, left_cx, cy)

    # ビード受け溝（⑨: 短辺X±外壁面のY±10.4へ移設・軸z=boxローカル25.8=lidローカル1.5は不変。
    # X+はUSBスロット±6の外・X-はスリット帯z10..20.4の上で干渉なし）
    groove_z = BOX_H - SKIRT_ENGAGE + BEAD_Z_LID   # 32-7.7+1.5 = 25.8（=lidローカル1.5）
    for sx in (-1, +1):
        axis_x = sx * (FOOT_X / 2 + GROOVE_R - GROOVE_DEPTH)          # ±30.80
        for sy in (-1, +1):
            part -= capsule_y(axis_x, sy * BEAD_YC, groove_z, GROOVE_R, BEAD_LEN)


    # （v3: box磁石ポケット+ボスは削除。shell2個のみ・§8-4）
    part = chamfer_bottom(part)

    # shell-boxスナップビード（2026-08-30②: ネック外面Y±・shellパラペット溝と対）
    # 台座0.25+ノーズR0.6の2段（パラメータ節の注記参照）。
    # ※接地面取りの後に足す（ビード下端が面取り帯0.5と重なりOCC chamferが失敗するため）
    # ※下端はz0.55でフラットカット: 面取り帯(0..0.5)の上に張り出す第1〜3層が線1本未満の
    #   棚になり形が出ない（check_thin_walls実測FAIL）。0.55なら壁面が全厚に戻った直上で、
    #   真下に45°面取り斜面が来るため実質支持される
    for sy in (-1, +1):
        face = sy * (FOOT_Y / 2 - NECK_INSET)                     # ±14.75
        for sx in (-1, +1):
            part += cbox(SB_BEAD_LEN + 0.8, 0.55, 0.55, 1.7,
                         sx * SB_BEAD_XC, face + sy * 0.275)      # 台座 14.45..15.00
            nose = capsule_x(sx * SB_BEAD_XC, face + sy * 0.20,   # ノーズ軸14.95(台座に0.05埋め)
                             SB_BEAD_Z, SB_BEAD_R, SB_BEAD_LEN)
            part += nose & cbox(SB_BEAD_LEN + 4, 4.0, 0.55, 3.0,
                                sx * SB_BEAD_XC, face)
    return part


# ============================================================
# lid（かぶせ蓋・スカート7.7・滑らか半円ビード）
# ============================================================
def build_lid():
    # ⑨: 長辺(Y±)は箱と同輪郭60.3x33.5で面一の板（四隅ともリム上に着座＝張り出しゼロ）。
    # X±だけ端タブ(→64.0)+スカート脚+ビードで係合し、Y位置決めは下垂フィン2枚が担う
    part = rounded_prism(FOOT_X, FOOT_Y, SKIRT_ENGAGE, SKIRT_ENGAGE + LID_PLATE, r=CORNER_R)
    for sx in (-1, +1):   # 端タブ（boxウィングパッド/脚と面一の±32.0まで張り出し）
        part += cbox(WING + 0.5, 2 * LEG_HALF_SPAN, SKIRT_ENGAGE, SKIRT_ENGAGE + LID_PLATE,
                     sx * (FOOT_X / 2 - 0.5 + (WING + 0.5) / 2))

    # スカート脚（X±・外面±32.0=タブと面一・内面±30.4=箱壁30.15+clr0.25）。
    # 中央切欠き±7.0はX+がUSBプラグの逃げ・X-が指掛かり（対称）。切欠きの上
    # (lidローカル5.2..7.7=box局所29.5..32)は全幅連結でフープ剛性を保つ
    leg_in = FOOT_X / 2 + LID_CLR                                  # 30.4
    for sx in (-1, +1):
        leg = cbox(SKIRT_T, 2 * LEG_HALF_SPAN, 0, SKIRT_ENGAGE + 1,
                   sx * (leg_in + SKIRT_T / 2))
        leg -= cbox(SKIRT_T + 2, 2 * LEG_CUT_HALF, -1, LEG_CUT_H,
                    sx * (leg_in + SKIRT_T / 2))
        part += leg

    # 滑らか半円カプセルビード（§8-4①の断面は実証済みのまま: R1.0・突出0.6・食い込み0.35。
    # ⑨でX±脚の内面へ移設・Y±10.4）
    for sx in (-1, +1):
        axis_x = sx * (leg_in + BEAD_R - BEAD_PROUD)               # ±30.8
        for sy in (-1, +1):
            part += capsule_y(axis_x, sy * BEAD_YC, BEAD_Z_LID, BEAD_R, BEAD_LEN)

    # Y位置決めフィン（⑨: Y側スカート廃止の代替。箱内壁14.75にclr0.30で沿う。
    # 脚が5.4mm先に係合してX/回転を拘束してからフィンが入る。先端box局所29.7=
    # ピン上端25.8・モジュール上面25.9より3.8上・lid→devkitcゲートで検証）
    for sy in (-1, +1):
        fin = cbox(FIN_LEN, FIN_T, SKIRT_ENGAGE - FIN_DROP, SKIRT_ENGAGE + 1,
                   0, sy * (IN_Y / 2 - FIN_CLR - FIN_T / 2))
        # 先端リードは壁側の外側1辺のみ0.3（両側0.4だと先端平坦が0.4=線1本未満の
        # スライバーになりcheck_thin_walls FAIL・実測）→ 平坦0.9を残す
        bot_out = [e for e in fin.edges().group_by(Axis.Z)[0]
                   if (abs(e.bounding_box().min.Y) > IN_Y / 2 - FIN_CLR - 0.1
                       and abs(e.bounding_box().max.Y) > IN_Y / 2 - FIN_CLR - 0.1)]
        try:
            fin = chamfer(bot_out, length=0.3)
        except ValueError:
            print("[warn] フィン先端の面取り失敗: 角のまま続行")
        part += fin

    # 押さえ六角筒2本（ハニカムセルの下方延長・2026-08-30③改2。孔は後段で全セル一括カット
    # =筒も貫通ベント。リム接触は押さえパッドギャップ検証ゲートで再確認）
    pad_len = BOX_H - (MODULE_TOP + PRESS_GAP)
    pad_z0 = SKIRT_ENGAGE - pad_len
    r_tube = HEX_PITCH / 3 ** 0.5
    for cx in PRESS_PAD_XC:
        part += extrude(Pos(cx, 0, pad_z0) * RegularPolygon(r_tube, 6),
                        amount=SKIRT_ENGAGE - pad_z0 + 1)

    # 反転印刷の接地面（プレート上面=モデルZ最上端）のエレファントフット対策（監査是正:
    # box/shellはchamfer_bottom適用済みなのにlidだけ未対策だった）
    # ※放熱孔より先に面取りする（孔リム多数へのOCC面取りは失敗しやすい）
    top_edges = part.edges().group_by(Axis.Z)[-1]
    for ln in (0.5, 0.4, 0.3):
        try:
            part = chamfer(top_edges, length=ln)
            break
        except ValueError:
            continue
    else:
        print("[warn] lidプレート上縁の面取り失敗: スライサーのelephant foot補正で代替")

    # 放熱ハニカム孔（2026-08-30③改2: 規則六角格子。⑧でカット対象をX-側のセルのみに限定
    # =CPU側23孔・Y対称は維持。X+側はESP32の赤LED直上になるため無孔の目隠し（レイ指示。
    # 排気はCPU直上23孔≈319mm2で給気側スリット+配線穴より依然大きい=ボトルネックにならない）。
    # 押さえ筒セルも同じ孔を貫通させる=CPU直上ベント。反転印刷で孔壁は垂直=きれいに出る）
    r_hole = HEX_HOLE_F / 3 ** 0.5
    row_dy = HEX_PITCH * 3 ** 0.5 / 2                             # 4.85
    for j in (-2, -1, 0, 1, 2):
        if j % 2 == 0:
            xs = [s * (HEX_PITCH / 2 + HEX_PITCH * k) for k in range(5) for s in (-1, +1)]
        else:
            xs = [0.0] + [s * HEX_PITCH * k for k in range(1, 5) for s in (-1, +1)]
        for gx in xs:
            if gx > -0.1:                # ⑧: LED側(X+)と中心列x=0は孔なし
                continue
            part -= extrude(Pos(gx, j * row_dy, pad_z0 - 1) * RegularPolygon(r_hole, 6),
                            amount=SKIRT_ENGAGE + LID_PLATE - pad_z0 + 3)
    return part


# ============================================================
# shell（外殻: 壁+パラペット+底リング+センサークレードル+boxコルベル+刻印）
# ============================================================
def build_shell(node_id):
    outer = rounded_prism(FOOT_X, FOOT_Y, 0, PARA_TOP)
    cav1 = cbox(IN_X, IN_Y, RING_T, BASE_H + 0.01)
    cav1 = fillet(cav1.edges().filter_by(Axis.Z), radius=1.5)
    cav2 = cbox(PARA_IN_X, PARA_IN_Y, BASE_H - 0.5, PARA_TOP + 1)
    cav2 = fillet(cav2.edges().filter_by(Axis.Z), radius=2.0)
    opening = cbox(IN_X - 2 * RING_W, IN_Y - 2 * RING_W, -1, RING_T + 1)
    opening = fillet(opening.edges().filter_by(Axis.Z), radius=1.5)
    part = outer - cav1 - cav2 - opening

    # box受けコルベル4個（§8-4②: パラペット内壁Y±・X±14・上面24.5・張り出し1.5）
    # 段2つ（0.75ずつ）で45°則内。boxネック縁(±14.75)を1.0受ける
    for cx in (-14.0, 14.0):
        for sy in (-1, +1):
            face = sy * PARA_IN_Y / 2                     # ±15.25
            for z0, z1, prot in ((23.2, CORBEL_TOP, CORBEL_PROT), (21.9, 23.35, CORBEL_PROT / 2)):
                part += cbox(8.0, prot + 1.0, z0, z1,
                             cx, face - sy * (prot + 1.0) / 2 + sy * 1.0)

    # shell-boxスナップ受け溝（2026-08-30②: パラペット内面Y±・boxネックビードと対。
    # 溝はワールド25.4・深0.5→溝底15.75。ビード先端15.55との半径スラック0.2・上唇0.35。
    # パラペット上縁のリード面取りは上唇を食い潰すため付けない=丸ビードの自己リードで入る）
    sb_groove_z = CORBEL_TOP + SB_BEAD_Z                              # 25.4
    for sy in (-1, +1):
        ay = sy * (PARA_IN_Y / 2 - (SB_GROOVE_R - SB_GROOVE_DEPTH))   # ±14.80
        for sx in (-1, +1):
            part -= capsule_x(sx * SB_BEAD_XC, ay, sb_groove_z, SB_GROOVE_R, SB_BEAD_LEN)

    # --- SHT31 クレードル（上から落とし込み・§8-4④） ---
    # 床ストリップ（Z0から立てて接地させる=ブリッジ無し。底面取りは掛けない→outer_only）
    for sy in (-1, +1):
        part += cbox(FLANK_X1 - FLANK_X0 + 0.2, 8.7, 0, RING_T, (FLANK_X0 + FLANK_X1) / 2, sy * 7.25)  # s1: リングからフランク壁下へ
        part += cbox(2.1, 5.1, 0, RING_T, 9.05, sy * 9.05)   # s2: -Xストップ壁下へ
        part += cbox(2.2, 2.2, 0, RING_T, 17.0, sy * 3.1)    # s4: タブ脇フランク下へ（s1と重なり接続）
    part += cbox(4.0, 6.0, 0, RING_T, 22.6, 0.0)             # s3: タブ先席+リブ下へ（+Xリングに接続）

    # 後席ポスト2（基板ベース後縁の下面を受ける。ハウジングコラム(X≤12.6)と脚(X≤13.7)の外）
    for sy in (-1, +1):
        part += cbox(1.9, 3.4, RING_T - 1, SHT_SEAT_Z, 14.95, sy * 5.1)
    # タブ先席+エンドストップ（素子(X17.6..20.4)より+X側。タブ先端22.0を0.3先で止める）
    # 2026-08-30①: 先端ツメのチークを載せるため席・壁をY±3.0へ拡幅
    part += cbox(2.3, 6.0, RING_T - 1, SHT_SEAT_Z, 22.05, 0.0)          # 席 X20.9..23.2
    part += cbox(1.2, 6.0, RING_T - 1, CRADLE_TOP, 22.9, 0.0)           # 壁 X22.3..23.5（接地・肉厚1.2）
    # 先端ツメ（2026-08-30①: タブ浮き上がりの押さえ。ストップ壁面22.3から張り出し1.0）
    # チーク2枚(タブY±2.0に片側0.2の案内隙間)の間にY方向ブリッジで天井を渡す=宙吊り印刷なし。
    # 天井下面はタブ上面9.1+0.35（第1ブリッジ層の垂れ0.1〜0.2を見込む）。入口側は0.3高い
    # 段付きで差し込みリード。挿入は「タブを天井下へ差し込み→後端を落とす」（ゲートで検証）
    for sy in (-1, +1):
        part += cbox(2.4, 0.8, RING_T - 1, 10.5, 22.3, sy * 2.6)        # チーク X21.1..23.5 Y2.2..3.0
    part += cbox(1.8, 6.0, 9.45, 10.5, 22.6, 0.0)                       # 天井段1 X21.7..23.5（押さえ面）
    part += cbox(2.2, 6.0, 9.75, 10.5, 22.4, 0.0)                       # 天井段2 X21.3..23.5（全長1.0）
    # タブ両脇フランク壁+ナブ（基板+ハウジングのCGは-X寄りで3点座の外→タブ上面も
    # ナブで押さえてシーソー傾きを±3°程度に制限）。0.8mm壁はクーポン実印刷で失敗→
    # 1.2x1.6に増厚し、水平リブで床(s3)側へ接続して孤立柱をやめる（Matte層間対策）
    # 2026-08-30①: 壁一式を+X0.4逃がす（傾け挿入12°で基板後縁の面が旧位置X16.1の
    # 前上角を~0.2掠めるため。ゲートのpose分解で実測→包絡最大X16.4の外へ）
    for sy in (-1, +1):
        part += cbox(1.2, 1.6, RING_T - 1, CRADLE_TOP, 17.1, sy * 3.1)      # 壁 X16.5..17.7 Y2.3..3.9
        part += cbox(1.0, 0.6, 9.25, 9.85, 17.1, sy * 2.1)                  # ナブ主段（先端Y1.8・張出0.5）
        part += cbox(1.0, 0.35, 9.85, 10.05, 17.1, sy * 2.225)              # ナブ上段リード（先端Y2.05）
        part += cbox(4.2, 1.2, RING_T - 1, 7.4, 19.5, sy * 3.1)             # リブ X17.4..21.6 Y2.5..3.7
                                                                            # （素子Y±1.5の外・タブ降下路7.9より下）
    # フランク壁2（Y±7.35..8.95=肉厚1.6でベースを案内）+ 保持ナブ + 後席への接続リブ
    for sy in (-1, +1):
        part += cbox(FLANK_X1 - FLANK_X0, FLANK_Y1 - FLANK_Y0, RING_T - 1, CRADLE_TOP,
                     (FLANK_X0 + FLANK_X1) / 2, sy * (FLANK_Y0 + FLANK_Y1) / 2)
        # ナブ主段: 張り出し0.55・食い込み0.20/側（2026-08-30①: 固定緩い→0.15から増。
        # 0.2超はFR-4が逃げない+Matte層間の欠けリスクでadvisor裁定の上限）・高さ0.6=3層
        part += cbox(2.0, 0.75, 9.25, 9.85, 14.95, sy * 7.175)              # 先端Y6.80（根元は壁内）
        part += cbox(2.0, 0.4, 9.85, 10.05, 14.95, sy * 7.25)               # 上段リード（先端Y7.05）
        # 後席ポストへの水平リブ（孤立壁をやめて面で支える。ハウジングY≤6.5の外）
        part += cbox(1.3, 1.2, RING_T - 1, 7.4, 14.95, sy * 7.25)           # Y6.65..7.85
    # -Xストップ壁2（基板前縁X10を0.2先で受ける。ハウジング(Y≤6.5)の外=Y6.8..10.5）
    # クーポン実測とMatte層間補正で1.2→1.6に増厚（係合壁の下限）
    for sy in (-1, +1):
        part += cbox(1.6, 3.7, RING_T - 1, CRADLE_TOP, 9.0, sy * 8.65)

    # 通気スリット（縦・側面X±のみ）
    for sx in (-1, +1):
        wall_cx = sx * (IN_X / 2 + WALL / 2)
        for cy in (-6.0, 0.0, 6.0):
            part -= cbox(WALL + 2, SLIT_W, 4.0, 14.0, wall_cx, cy)

    # 磁石ポケット（2026-08-30⑤: ±19.5の独立2個へ。磁石どうしの引き寄せ対策・関数docstring参照）
    for cx in (-19.5, +19.5):
        part = magnet_pocket(part, cx, 9.5, boss_zmax=16.8)
    part = chamfer_bottom(part, outer_only=True)   # 細い床ストリップの第1層を痩せさせない

    # ノードID刻印（底面前バンド・下から正読・深さ0.7）
    # フォント刻印は数字のテーパー/カウンターが「残り材<0.55の島・舌」になり形が出ない
    # （Arial Bold「4」の閉カウンター、Consolas「4」の合流くさび、いずれもcheck_thin_walls
    # 実測FAIL・2026-08-30）→ 軸平行ストロークの手組みグリフに置換。残り材の最小幅を
    # 設計で保証: 縁マージン1.2（底リング前バンド幅6.0・面取り0.5後も第1層0.7で舌長<1.5）
    # ／グリフ内0.9（hard0.55に余裕・soft0.8未満のWARNは化粧領域として許容）／字間1.4
    ENGRAVE_D = 0.7
    STROKES = {              # 文字ローカル座標 (cx, cy, w, h)。y上向き=正読。字箱x±1.3
                             # 溝幅0.6（<0.45だと溝側の形が出ない）
        "n": [(-1.0, -0.5, 0.6, 2.6), (0.0, 0.5, 2.6, 0.6), (1.0, -0.5, 0.6, 2.6)],
        "1": [(0.0, 0.0, 0.6, 3.6)],
        "2": [(0.0, 1.5, 2.6, 0.6), (1.0, 0.75, 0.6, 2.1), (0.0, 0.0, 2.6, 0.6),
              (-1.0, -0.75, 0.6, 2.1), (0.0, -1.5, 2.6, 0.6)],
        "3": [(0.0, 1.5, 2.6, 0.6), (0.0, 0.0, 2.6, 0.6), (0.0, -1.5, 2.6, 0.6),
              (1.0, 0.0, 0.6, 3.6)],
        "4": [(-1.0, 0.75, 0.6, 2.1), (0.0, 0.0, 2.6, 0.6), (1.0, 0.0, 0.6, 3.6)],
    }
    txt_plane = Plane(origin=(0, -(FOOT_Y / 2 - 3.0), 0), x_dir=(1, 0, 0), z_dir=(0, 0, -1))
    for ch, xc in zip(node_id, (-2.0, 2.0)):
        for cx, cy, w, h in STROKES[ch]:
            part -= txt_plane * Pos(xc + cx, cy, -ENGRAVE_D / 2) * Box(w, h, ENGRAVE_D)
    return part


# ============================================================
# 生成・出力
# ============================================================
if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"

    if which in ("box", "all"):
        p = build_box()
        export_stl(p, os.path.join(OUT, "node_case_v3_box.stl"))
        print("box bbox:", p.bounding_box().size)

    if which in ("lid", "all"):
        p = build_lid()
        export_stl(p, os.path.join(OUT, "node_case_v3_lid.stl"))
        print("lid bbox:", p.bounding_box().size)

    if which in ("shell", "all"):
        for nid in (NODE_IDS if which == "all" else NODE_IDS[:1]):
            p = build_shell(nid)
            export_stl(p, os.path.join(OUT, f"node_case_v3_shell_{nid}.stl"))
            print(f"shell {nid} bbox:", p.bounding_box().size)

    print("DONE")
