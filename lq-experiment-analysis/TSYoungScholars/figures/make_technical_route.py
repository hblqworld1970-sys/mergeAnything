#!/usr/bin/env python3
"""技术路线图（SVG，标准库）。画布 180 x 78 mm，与机制图同色系。"""
from pathlib import Path

OUT = Path(__file__).resolve().parent
W, H = 180.0, 78.0
PT = 0.3528
BLUE, GREEN, ORANGE, VERM = "#0072B2", "#009E73", "#E69F00", "#D55E00"
INK, MUTE, LINE = "#333333", "#6B6B6B", "#555555"
FONT = "'PingFang SC', 'Hiragino Sans GB', 'Heiti SC', Arial, sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=5.2, anchor="middle", weight="normal", fill=INK, spacing=None):
    fs, ls = size * PT, (spacing or size * 1.28) * PT
    buf = [f'<text font-family="{FONT}" font-size="{fs:.3f}" font-weight="{weight}" '
           f'fill="{fill}" text-anchor="{anchor}">']
    for i, ln in enumerate(s.split("\n")):
        buf.append(f'<tspan x="{x:.2f}" y="{y + i * ls:.3f}">{esc(ln)}</tspan>')
    buf.append("</text>")
    return "".join(buf)


def rect(x, y, w, h, r=2.4, fill="none", stroke=LINE, sw=0.45, op=1.0):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'rx="{r:.2f}" ry="{r:.2f}" fill="{fill}" fill-opacity="{op}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def arrow(x1, y1, x2, y2, color=LINE, sw=0.6):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" '
            f'marker-end="url(#ah)"/>')


boxes = [
    (6, 18, 38, 42, MUTE, "已完成", "公开图谱再分析\nSPP1⁺ TAM · B6 通路\nPPARG · CellChat"),
    (48, 18, 38, 42, BLUE, "2027 · 内容一", "基线队列 mIF\nSPP1⁺ PDXK⁺ 定位\n巨噬细胞 PLP 定量"),
    (90, 18, 38, 42, GREEN, "2028 · 内容二", "PLP–PPARγ–SPP1\nCD8 共培养拆解\n剥夺 vs 配体轴"),
    (132, 18, 42, 42, VERM, "2029 · 内容三", "髓系 PDXK / PPARγ\n联合抗 PD-1\nSPP1/PDXK/PPARG 评分"),
]

parts = [
    f'<?xml version="1.0" encoding="UTF-8"?>',
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
    '<defs><marker id="ah" viewBox="0 0 10 10" refX="9.2" refY="5" markerWidth="3.2" '
    'markerHeight="3.2" orient="auto" markerUnits="userSpaceOnUse">'
    f'<path d="M0.5,1 L9.5,5 L0.5,9 L2.4,5 z" fill="{LINE}"/></marker></defs>',
    f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>',
    text(90, 8.8, "技术路线（2027–2029）", size=7.2, weight="bold"),
]
for i, (x, y, w, h, col, title, body) in enumerate(boxes):
    parts.append(rect(x, y, w, h, r=3.2, fill=col, stroke=col, sw=0.55, op=0.09))
    parts.append(rect(x, y, 3.0, h, r=1.2, fill=col, stroke=col, sw=0.0, op=1.0))
    parts.append(text(x + w / 2 + 0.6, y + 9.2, title, size=5.5, weight="bold", fill=col))
    parts.append(text(x + w / 2 + 0.6, y + 18.8, body, size=5.0, fill=INK, spacing=6.0))
    if i < 3:
        x1 = x + w + 0.6
        x2 = boxes[i + 1][0] - 0.8
        parts.append(arrow(x1, y + h / 2, x2, y + h / 2))

parts.append(text(90, 70.2,
                  "主线：区室化 B6 陷阱 → PPARγ–SPP1 锁定 → CD8 干性丧失 / 耗竭 → 抗 PD-1 原发耐药",
                  size=4.8, fill=MUTE))
parts.append(text(90, 75.4,
                  "干预点：髓系限定 PDXK（4-DP 等）· PPARγ（遗传与 GW9662 互证）· 下游读出 SPP1–CD44 / ITGA4",
                  size=4.6, fill=MUTE))
parts.append("</svg>\n")
(OUT / "technical_route_CN.svg").write_text("\n".join(parts), encoding="utf-8")
print("wrote", OUT / "technical_route_CN.svg")
