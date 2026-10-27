"""
生成站点占位素材（SVG 插图 / OG 图 / favicon / 简历占位 PDF）。

用法：
    python scripts/gen_assets.py
生成结果写入 public/ 与 public/img/。
这些图只是「版式占位」，上线前换成你真实的原理图、PCB 截图和实物照片即可。
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
IMG = PUB / "img"
PUB.mkdir(exist_ok=True)
IMG.mkdir(exist_ok=True)

MONO = "JetBrains Mono, SFMono-Regular, Consolas, monospace"


# ---------------------------------------------------------------------------
# PCB 风格
# ---------------------------------------------------------------------------
def pcb(width=1600, height=1000, seed=7, title="ENV-NODE v1.2", chips=None):
    rnd = random.Random(seed)
    chips = chips or [
        (610, 360, 250, 250, "U1", "STM32F103"),
        (960, 170, 210, 170, "U2", "ESP-01S"),
        (250, 200, 180, 150, "U3", "SHT30"),
        (250, 620, 150, 120, "U4", "OLED"),
        (980, 620, 260, 160, "U5", "PWR"),
    ]

    bx, by, bw, bh = 34, 26, 1532, 948
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="PCB 布局示意图">',
        "<defs>"
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#08110f"/><stop offset="1" stop-color="#0c1714"/>'
        "</linearGradient>"
        f'<linearGradient id="board" x1="0" y1="0" x2="0.6" y2="1">'
        f'<stop offset="0" stop-color="#107a4b"/><stop offset="0.55" stop-color="#0d5f3a"/>'
        f'<stop offset="1" stop-color="#0b4c2f"/></linearGradient>'
        f'<radialGradient id="glow" cx="0.25" cy="0.15" r="0.8">'
        f'<stop offset="0" stop-color="#7ff0c0" stop-opacity="0.16"/>'
        f'<stop offset="1" stop-color="#7ff0c0" stop-opacity="0"/></radialGradient>'
        "</defs>",
        f'<rect width="{width}" height="{height}" fill="url(#bg)"/>',
        # 板子
        f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="30" fill="url(#board)" '
        f'stroke="#0a3f28" stroke-width="3"/>',
        f'<rect x="{bx + 18}" y="{by + 18}" width="{bw - 36}" height="{bh - 36}" rx="20" '
        f'fill="none" stroke="#39b981" stroke-opacity="0.35" stroke-width="2"/>',
    ]

    # 走线
    def trace():
        x = rnd.randrange(bx + 50, bx + bw - 50, 20)
        y = rnd.randrange(by + 50, by + bh - 50, 20)
        pts = [(x, y)]
        for _ in range(rnd.randint(2, 4)):
            if rnd.random() < 0.5:
                x = min(max(x + rnd.choice([-1, 1]) * rnd.randrange(60, 320, 20),
                            bx + 40), bx + bw - 40)
            else:
                y = min(max(y + rnd.choice([-1, 1]) * rnd.randrange(60, 320, 20),
                            by + 40), by + bh - 40)
            pts.append((x, y))
        d = "M" + " L".join(f"{px} {py}" for px, py in pts)
        w = rnd.choice([2, 2, 3, 4])
        return (f'<path d="{d}" fill="none" stroke="#2fbd85" stroke-opacity="0.5" '
                f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

    out += [trace() for _ in range(46)]

    # 焊盘阵列
    for cx, cy in [(1150, 430), (1150, 480), (1150, 530)]:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="11" fill="#c9922f" stroke="#7a5518"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="4.5" fill="#0a2e1d"/>')

    # 元件
    for cx, cy, w, h, ref, name in chips:
        out.append(
            f'<rect x="{cx}" y="{cy}" width="{w}" height="{h}" rx="8" fill="#0b1720" '
            f'stroke="#39b981" stroke-opacity="0.45" stroke-width="2"/>'
        )
        # 引脚
        step = 22
        for i in range(int(w // step) - 2):
            px = cx + step + i * step
            out.append(f'<rect x="{px}" y="{cy - 9}" width="9" height="9" fill="#c9922f"/>')
            out.append(f'<rect x="{px}" y="{cy + h}" width="9" height="9" fill="#c9922f"/>')
        for i in range(int(h // step) - 2):
            py = cy + step + i * step
            out.append(f'<rect x="{cx - 9}" y="{py}" width="9" height="9" fill="#c9922f"/>')
            out.append(f'<rect x="{cx + w}" y="{py}" width="9" height="9" fill="#c9922f"/>')
        out.append(
            f'<text x="{cx + w / 2}" y="{cy + h / 2 - 4}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="20" fill="#d5f5e6" fill-opacity="0.92">{name}</text>'
        )
        out.append(
            f'<text x="{cx + w / 2}" y="{cy + h / 2 + 20}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="15" fill="#8fe0ba" fill-opacity="0.7">{ref}</text>'
        )

    # 丝印
    out.append(
        f'<text x="{bx + 34}" y="{by + 52}" font-family="{MONO}" font-size="26" '
        f'fill="#eafff4" fill-opacity="0.9" letter-spacing="3">{title}</text>'
    )
    out.append(
        f'<text x="{bx + 34}" y="{by + bh - 26}" font-family="{MONO}" font-size="17" '
        f'fill="#bdf0d6" fill-opacity="0.6" letter-spacing="2">'
        f"50 x 40 mm  ·  2 LAYER  ·  REV A</text>"
    )
    out.append(f'<rect width="{width}" height="{height}" fill="url(#glow)"/>')
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------------------
# 原理图风格
# ---------------------------------------------------------------------------
def schematic(width=1600, height=1000):
    ink = "#17202b"
    soft = "#64748b"
    blue = "#1f6feb"

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="环境监测节点原理图节选">',
        f'<rect width="{width}" height="{height}" fill="#fbfcfd"/>',
    ]
    # 网格
    for x in range(0, width, 20):
        out.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="#e6ebf1" stroke-width="1"/>')
    for y in range(0, height, 20):
        out.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#e6ebf1" stroke-width="1"/>')

    def wire(pts, color=ink, w=2):
        d = "M" + " L".join(f"{x} {y}" for x, y in pts)
        return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'

    def label(x, y, text, size=19, color=soft, anchor="start", weight="400"):
        return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{color}" '
                f'text-anchor="{anchor}" font-weight="{weight}">{text}</text>')

    def block(x, y, w, h, title, sub=""):
        parts = [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#ffffff" '
            f'stroke="{ink}" stroke-width="2"/>',
            label(x + w / 2, y + h / 2 - 2, title, 21, ink, "middle", "600"),
        ]
        if sub:
            parts.append(label(x + w / 2, y + h / 2 + 24, sub, 16, soft, "middle"))
        return "".join(parts)

    # MCU
    out.append(block(600, 330, 300, 340, "STM32F103", "C8T6"))
    for i in range(6):
        y = 380 + i * 46
        out.append(wire([(560, y), (600, y)]))
        out.append(label(552, y + 5, ["VDD", "GND", "PA9", "PA10", "PB6", "PB7"][i], 15, soft, "end"))
    for i in range(4):
        y = 370 + i * 60
        out.append(wire([(900, y), (940, y)]))
        out.append(label(948, y + 5, ["TX", "RX", "SCL", "SDA"][i], 15, soft, "start"))

    # 传感器
    out.append(block(170, 300, 220, 130, "SHT30", "I2C 0x44"))
    out.append(wire([(390, 365), (520, 365), (520, 380), (560, 380)]))
    out.append(wire([(390, 405), (540, 405), (540, 426), (560, 426)]))

    # 上拉电阻
    out.append(wire([(520, 340), (520, 300), (470, 300)]))
    out.append(f'<rect x="452" y="272" width="36" height="28" fill="none" stroke="{ink}" stroke-width="2"/>')
    out.append(label(470, 258, "4.7k", 15, soft, "middle"))
    out.append(wire([(452, 300), (410, 300), (410, 240), (520, 240), (520, 300)]))

    # ESP 模块
    out.append(block(1000, 300, 250, 150, "ESP-01S", "AT 固件"))
    out.append(wire([(940, 370), (1000, 370)]))
    out.append(wire([(940, 395), (1000, 395)]))

    # 天线
    out.append(wire([(1250, 375), (1330, 375)], blue))
    for i in range(4):
        out.append(wire([(1330, 345), (1330, 405)], blue, 3))
        out.append(wire([(1330, 345 + i * 20), (1372, 345 + i * 20)], blue, 3))

    # 电源
    out.append(block(170, 640, 240, 130, "AMS1117-3.3"))
    out.append(wire([(290, 640), (290, 480), (600, 480)]))
    out.append(label(300, 620, "5V → 3.3V", 16, soft))
    out.append(wire([(410, 705), (520, 705), (520, 670), (600, 670)]))

    # 去耦
    for i, x in enumerate([1000, 1080, 1160]):
        out.append(wire([(x, 520), (x, 560)]))
        out.append(f'<line x1="{x - 22}" y1="560" x2="{x + 22}" y2="560" stroke="{ink}" stroke-width="2"/>')
        out.append(f'<line x1="{x - 22}" y1="574" x2="{x + 22}" y2="574" stroke="{ink}" stroke-width="2"/>')
        out.append(wire([(x, 574), (x, 620)]))
        out.append(label(x, 648, "100nF", 14, soft, "middle"))

    # 标题栏
    out.append(f'<line x1="60" y1="880" x2="1540" y2="880" stroke="{ink}" stroke-width="2"/>')
    out.append(label(60, 918, "ENV-NODE  /  SHEET 1 OF 2  /  REV A", 20, ink, "start", "600"))
    out.append(label(1540, 918, "DRAWN BY LI MING  ·  2026.04", 18, soft, "end"))
    out.append(label(60, 62, "环境监测节点 · 原理图（节选）", 26, ink, "start", "600"))
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------------------
# 系统架构图
# ---------------------------------------------------------------------------
def arch(width=1600, height=1000):
    ink = "#17202b"
    soft = "#64748b"
    blue = "#1f6feb"
    green = "#00a878"

    nodes = [
        (90, 250, "SHT30", "温湿度传感器", soft),
        (370, 250, "STM32F103", "采样 + 滤波", ink),
        (660, 250, "ESP-01S", "WiFi / AT", blue),
        (950, 250, "EMQX", "自建 MQTT Broker", green),
        (1240, 250, "云数据库", "MySQL", soft),
    ]

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="系统架构图">',
        "<defs>"
        f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0 0 L10 5 L0 10 z" fill="{soft}"/></marker></defs>',
        f'<rect width="{width}" height="{height}" fill="#fbfcfd"/>',
    ]
    for x in range(0, width, 24):
        out.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="#eef2f6"/>')
    for y in range(0, height, 24):
        out.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#eef2f6"/>')

    out.append(
        f'<text x="90" y="130" font-family="{MONO}" font-size="24" fill="{ink}" '
        f'font-weight="600">系统链路：传感器 → 主控 → 通信 → 云端 → 应用</text>'
    )

    for x, y, title, sub, color in nodes:
        out.append(
            f'<rect x="{x}" y="{y}" width="230" height="106" rx="8" fill="#ffffff" '
            f'stroke="{color}" stroke-width="2"/>'
        )
        out.append(
            f'<text x="{x + 115}" y="{y + 46}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="20" fill="{ink}" font-weight="600">{title}</text>'
        )
        out.append(
            f'<text x="{x + 115}" y="{y + 76}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="15" fill="{soft}">{sub}</text>'
        )

    for i in range(len(nodes) - 1):
        x1 = nodes[i][0] + 230
        x2 = nodes[i + 1][0]
        y = nodes[i][1] + 53
        out.append(
            f'<line x1="{x1 + 4}" y1="{y}" x2="{x2 - 10}" y2="{y}" stroke="{soft}" '
            f'stroke-width="2" marker-end="url(#ar)"/>'
        )

    # 应用层
    apps = [(660, 560, "微信小程序"), (950, 560, "网页看板 / ECharts")]
    for x, y, t in apps:
        out.append(
            f'<rect x="{x}" y="{y}" width="230" height="86" rx="8" fill="#f4f7fa" '
            f'stroke="#cbd5e1" stroke-width="2" stroke-dasharray="5 4"/>'
        )
        out.append(
            f'<text x="{x + 115}" y="{y + 50}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="17" fill="{ink}">{t}</text>'
        )
        out.append(
            f'<line x1="{x + 115}" y1="{y - 4}" x2="{x + 115}" y2="356" stroke="{soft}" '
            f'stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ar)"/>'
        )

    # 本地显示
    out.append(
        f'<rect x="370" y="560" width="230" height="86" rx="8" fill="#ffffff" '
        f'stroke="{soft}" stroke-width="2"/>'
    )
    out.append(
        f'<text x="485" y="610" text-anchor="middle" font-family="{MONO}" font-size="17" '
        f'fill="{ink}">OLED 本地显示</text>'
    )
    out.append(
        f'<line x1="485" y1="556" x2="485" y2="360" stroke="{soft}" stroke-width="2" '
        f'marker-end="url(#ar)"/>'
    )

    out.append(
        f'<text x="90" y="810" font-family="{MONO}" font-size="16" fill="{soft}">'
        f"采样 100ms  ·  上报 5s  ·  QoS 1  ·  断线指数退避重连</text>"
    )
    out.append(
        f'<text x="90" y="850" font-family="{MONO}" font-size="16" fill="{soft}">'
        f"端到端延迟平均 300ms  ·  连续运行 72h  ·  丢包率 0.4%</text>"
    )
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------------------
# 示波器 / 曲线
# ---------------------------------------------------------------------------
def waveform(width=1600, height=1000, seed=3):
    rnd = random.Random(seed)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="I2C 时序与温度曲线">',
        f'<rect width="{width}" height="{height}" fill="#0a0e14"/>',
    ]
    for x in range(0, width, 40):
        out.append(f'<line x1="{x}" y1="0" x2="{x}" y2="520" stroke="#141c26"/>')
    for y in range(0, 520, 40):
        out.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#141c26"/>')

    out.append(
        f'<text x="40" y="46" font-family="{MONO}" font-size="17" fill="#7d8b9c">'
        f"CH1 2.00V/div  CH2 2.00V/div  TIME 100µs/div</text>"
    )

    # 方波 SCL
    y_hi, y_lo = 130, 220
    pts = []
    x = 90
    while x < 1180:
        pts += [(x, y_lo), (x, y_hi), (x + 70, y_hi), (x + 70, y_lo)]
        x += 70
    d = "M" + " L".join(f"{px} {py}" for px, py in pts)
    out.append(f'<path d="{d}" fill="none" stroke="#00e5a0" stroke-width="3"/>')
    out.append(
        f'<text x="40" y="112" font-family="{MONO}" font-size="15" fill="#00e5a0" fill-opacity="0.8">SCL</text>'
    )

    # 数据线 SDA（随机高低）
    y_hi2, y_lo2 = 290, 380
    pts = []
    x = 90
    prev = y_lo2
    while x < 1180:
        w = rnd.choice([70, 140])
        pts += [(x, prev), (x + w, prev)]
        prev = y_lo2 if prev == y_hi2 else y_hi2
        x += w
    d = "M" + " L".join(f"{px} {py}" for px, py in pts)
    out.append(f'<path d="{d}" fill="none" stroke="#4d9fff" stroke-width="3"/>')
    out.append(
        f'<text x="40" y="272" font-family="{MONO}" font-size="15" fill="#4d9fff" fill-opacity="0.8">SDA</text>'
    )

    # 分隔
    out.append(f'<line x1="40" y1="520" x2="1560" y2="520" stroke="#1f2a36" stroke-width="2"/>')

    # 温度曲线
    base = 760
    pts = []
    for i in range(0, 1520, 8):
        t = i / 1520 * math.tau * 2.2
        val = base - 70 - math.sin(t) * 46 - math.sin(t * 3.7) * 9 - rnd.uniform(0, 5)
        pts.append((40 + i, val))
    d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    out.append(f'<path d="{d}" fill="none" stroke="#4d9fff" stroke-width="3" stroke-opacity="0.9"/>')

    out.append(
        f'<text x="40" y="590" font-family="{MONO}" font-size="16" fill="#7d8b9c">'
        f"72h 温度曲线（每 5s 一个点，采样降频展示）</text>"
    )
    out.append(
        f'<text x="40" y="930" font-family="{MONO}" font-size="14" fill="#5b6675">'
        f"实测：±0.3℃  ·  丢包率 0.4%  ·  无重启</text>"
    )
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------------------
# OG 图 / favicon / 简历占位
# ---------------------------------------------------------------------------
def _font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


SANS = ["C:/Windows/Fonts/msyhbd.ttc", "C:/Windows/Fonts/msyh.ttc"]
MONOF = ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/consolab.ttf"]


def og_image():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#070c14")
    d = ImageDraw.Draw(img, "RGBA")

    for x in range(0, W, 28):
        for y in range(0, H, 28):
            d.ellipse((x, y, x + 1.6, y + 1.6), fill=(120, 200, 255, 30))

    # 光晕：右上蓝、左下青
    for r in range(440, 0, -12):
        a = int(26 * (1 - r / 440))
        d.ellipse((W - 260 - r, -180 - r, W - 260 + r, -180 + r), fill=(31, 143, 255, a))
    for r in range(300, 0, -10):
        a = int(18 * (1 - r / 300))
        d.ellipse((60 - r, H + 60 - r, 60 + r, H + 60 + r), fill=(79, 216, 255, a))

    f_name = _font(SANS, 96)
    f_role = _font(SANS, 34)
    f_small = _font(SANS, 26)
    f_mono = _font(MONOF, 24)

    d.text((80, 160), "潘赫", font=f_name, fill="#e8f1fa")
    d.text((84, 292), "物联网工程 2028 届", font=f_role, fill="#a3b6cb")
    d.text((84, 340), "嵌入式硬件 / 物联网方案", font=f_role, fill="#4fd8ff")

    d.ellipse((86, 424, 98, 436), fill="#35d6a4")
    d.text((112, 416), "寻找 2027 寒假实习", font=f_small, fill="#cfe4f5")

    d.line((80, 508, 1120, 508), fill=(96, 176, 255, 46), width=1)
    d.text((80, 534), "大连民族大学 · example.com", font=_font(SANS, 22), fill="#7c90a6")
    d.text((80, 576), "PCB · STM32 · ESP32 · MQTT", font=f_mono, fill="#5e7285")

    # 右侧终端方块
    bx, by, bw, bh = 700, 150, 420, 300
    d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=12,
                        fill=(5, 10, 18, 255), outline=(79, 216, 255, 60), width=1)
    d.rounded_rectangle((bx, by, bx + bw, by + 36), radius=12, fill=(79, 216, 255, 14))
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        d.ellipse((bx + 14 + i * 18, by + 14, bx + 24 + i * 18, by + 24), fill=c)

    lines = [
        ("$ whoami", "#4fd8ff", "#e8f1fa"),
        ("PAN HE · 2028", "#7c90a6", "#b6c9dc"),
        ("$ cat focus.txt", "#4fd8ff", "#e8f1fa"),
        ("hardware / IoT", "#7c90a6", "#b6c9dc"),
        ("$ ls projects/", "#4fd8ff", "#e8f1fa"),
        ("env-node line-car", "#7c90a6", "#b6c9dc"),
    ]
    y = by + 68
    for text, c1, c2 in lines:
        if text.startswith("$"):
            d.text((bx + 24, y), "$", font=f_mono, fill=c1)
            d.text((bx + 50, y), text[2:], font=f_mono, fill=c2)
        else:
            d.text((bx + 50, y), text, font=f_mono, fill=c2)
        y += 38

    img.save(PUB / "og.png", optimize=True)
    img.resize((180, 180), Image.LANCZOS).save(PUB / "apple-touch-icon.png")


def favicon():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <linearGradient id="g" x1="4" y1="2" x2="28" y2="30" gradientUnits="userSpaceOnUse">
      <stop stop-color="#8BEEFF"/><stop offset="1" stop-color="#2A86FF"/>
    </linearGradient>
  </defs>
  <rect width="32" height="32" rx="7" fill="#070C14"/>
  <path d="M16 5.4 25.2 10.7v10.6L16 26.6 6.8 21.3V10.7L16 5.4Z"
        fill="none" stroke="url(#g)" stroke-width="1.6" stroke-linejoin="round"/>
  <circle cx="16" cy="16" r="2.2" fill="url(#g)"/>
</svg>
"""
    (PUB / "favicon.svg").write_text(svg, encoding="utf-8")


def resume_placeholder():
    W, H = 1240, 1754
    img = Image.new("RGB", (W, H), "#ffffff")
    d = ImageDraw.Draw(img)
    f_big = _font(SANS, 54)
    f_mid = _font(SANS, 28)
    f_mono = _font(MONOF, 22)

    d.text((100, 150), "简历占位页", font=f_big, fill="#0f141b")
    d.text((100, 240), "把 public/resume-preview.pdf 换成你的真实简历 PDF", font=f_mid, fill="#5b6675")
    d.text((100, 290), "建议：一页、与主页口径一致、文件名 姓名-嵌入式硬件-2028届.pdf",
           font=f_mid, fill="#5b6675")

    d.line((100, 380, W - 100, 380), fill="#e3e8ef", width=2)

    blocks = [
        "教育背景 / Education",
        "专业技能 / Skills",
        "项目经历 / Projects",
        "竞赛与奖项 / Awards",
        "联系方式 / Contact",
    ]
    y = 440
    for b in blocks:
        d.rectangle((100, y, W - 100, y + 120), outline="#e3e8ef", width=2)
        d.text((124, y + 24), b, font=f_mono, fill="#8a94a6")
        y += 150

    d.text((100, H - 120), "PLACEHOLDER  ·  由 scripts/gen_assets.py 生成", font=f_mono, fill="#cbd5e1")
    img.save(PUB / "resume-preview.pdf", "PDF", resolution=110.0)


def main():
    (IMG / "pcb-env.svg").write_text(
        pcb(seed=11, title="ENV-NODE  v1.2",
            chips=[(610, 360, 250, 250, "U1", "STM32F103"),
                   (980, 170, 210, 170, "U2", "ESP-01S"),
                   (250, 200, 180, 150, "U3", "SHT30"),
                   (250, 620, 150, 120, "U4", "OLED"),
                   (980, 620, 260, 160, "U5", "PWR")]),
        encoding="utf-8",
    )
    (IMG / "pcb-car.svg").write_text(
        pcb(seed=23, title="LINE-CAR  v2.0",
            chips=[(600, 200, 240, 220, "U1", "STM32F103"),
                   (950, 560, 300, 200, "U2", "TB6612"),
                   (250, 240, 200, 180, "J1", "SENSOR"),
                   (250, 620, 200, 160, "J2", "MOTOR")]),
        encoding="utf-8",
    )
    (IMG / "pcb-door.svg").write_text(
        pcb(seed=37, title="DOOR-SENSOR  v1.0",
            chips=[(640, 420, 230, 230, "U1", "STM32L051"),
                   (330, 240, 210, 160, "U2", "SX1278"),
                   (200, 620, 150, 110, "SW1", "REED"),
                   (1000, 620, 190, 120, "BT1", "CR2032")]),
        encoding="utf-8",
    )
    (IMG / "schematic-env.svg").write_text(schematic(), encoding="utf-8")
    (IMG / "arch-env.svg").write_text(arch(), encoding="utf-8")
    (IMG / "wave-env.svg").write_text(waveform(), encoding="utf-8")
    favicon()
    og_image()
    resume_placeholder()

    # 搜索引擎
    (PUB / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: https://example.com/sitemap.xml\n",
        encoding="utf-8",
    )
    print("assets written to", PUB)


if __name__ == "__main__":
    main()
