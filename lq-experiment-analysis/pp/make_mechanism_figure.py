#!/usr/bin/env python3
"""生成投稿级矢量机制图（SVG，纯标准库实现，无第三方依赖）。

用户单位 = 1 mm，画布 180 x 110 mm（双栏宽）。
文字以 <text> 元素保留，便于在 Illustrator / Inkscape 中直接编辑。

用法：
    python3 make_mechanism_figure.py            # 同时输出中英文两版
"""

from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent

W, H = 180.0, 110.0

# Okabe-Ito 色盲友好配色
BLUE = "#0072B2"      # 维生素 B6 / 代谢
GREEN = "#009E73"     # PPARγ / 细胞核
ORANGE = "#E69F00"    # SPP1
VERM = "#D55E00"      # 干预
PURPLE = "#CC79A7"    # Treg
SKY = "#56B4E9"       # CD8 T / NK
INK = "#333333"
MUTE = "#7A7A7A"
LINE = "#555555"

PT = 0.3528  # 1 pt = 0.3528 mm

FONT_EN = "Arial, Helvetica, 'Helvetica Neue', sans-serif"
FONT_CN = "'PingFang SC', 'Hiragino Sans GB', 'Heiti SC', Arial, sans-serif"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Svg:
    def __init__(self, font):
        self.parts = []
        self.font = font

    def add(self, s):
        self.parts.append(s)

    # ---------- 基本图元 ----------
    def rect(self, x, y, w, h, r=2.5, fill="none", stroke=LINE, sw=0.45,
             fill_opacity=1.0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
                 f'rx="{r:.2f}" ry="{r:.2f}" fill="{fill}" fill-opacity="{fill_opacity}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def ellipse(self, cx, cy, rx, ry, fill, stroke=None, sw=0.4):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" '
                 f'fill="{fill}"{st}/>')

    def circle(self, cx, cy, r, fill, stroke=None, sw=0.4):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}"{st}/>')

    def text(self, x, y, s, size=5.5, anchor="middle", weight="normal",
             fill=INK, style="normal", spacing=None):
        """多行文本。行内的 "⁺" 会被排成真正的上标 tspan——直接使用该
        Unicode 字符会在嵌入 Arial 的 PDF 中变成缺字方框。"""
        fs = size * PT
        ls = (spacing if spacing else size * 1.32) * PT
        sup_fs = fs * 0.66
        sup_dy = fs * 0.34
        # 整个 <text> 拼成单行字符串：元素之间若出现换行，SVG 会把空白
        # 折叠成一个空格，导致上标前后多出间隙。
        buf = [f'<text font-family="{self.font}" '
               f'font-size="{fs:.3f}" font-weight="{weight}" font-style="{style}" '
               f'fill="{fill}" text-anchor="{anchor}">']
        for i, ln in enumerate(s.split("\n")):
            # 每行使用绝对 y，避免上标的 dy 累积影响后续行
            ly = y + i * ls
            buf.append(f'<tspan x="{x:.2f}" y="{ly:.3f}">')
            segs = ln.split("⁺")
            buf.append(esc(segs[0]))
            for seg in segs[1:]:
                buf.append(f'<tspan dy="{-sup_dy:.3f}" font-size="{sup_fs:.3f}">+</tspan>')
                buf.append(f'<tspan dy="{sup_dy:.3f}">{esc(seg)}</tspan>')
            buf.append("</tspan>")
        buf.append("</text>")
        self.add("".join(buf))

    def line(self, x1, y1, x2, y2, stroke=LINE, sw=0.45, dash=None, cap="round"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                 f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{d}/>')

    def arrow(self, x1, y1, x2, y2, color=LINE, sw=0.55, dash=None, key=None):
        key = key or color_key(color)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                 f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{d} '
                 f'marker-end="url(#ah-{key})"/>')

    def path(self, d, color=LINE, sw=0.55, dash=None, arrow=True, key=None):
        key = key or color_key(color)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        mk = f' marker-end="url(#ah-{key})"' if arrow else ""
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
                 f'stroke-linecap="round" stroke-linejoin="round"{da}{mk}/>')

    def inhibit(self, x, y, angle=0, color=VERM, length=4.4, sw=0.7):
        """抑制符号：垂直于作用方向的短横杠。angle 为横杠自身角度（度）。"""
        import math
        a = math.radians(angle)
        dx, dy = math.cos(a) * length / 2, math.sin(a) * length / 2
        self.line(x - dx, y - dy, x + dx, y + dy, stroke=color, sw=sw, cap="butt")

    def render(self):
        colors = {"blue": BLUE, "green": GREEN, "orange": ORANGE, "verm": VERM,
                  "purple": PURPLE, "sky": SKY, "line": LINE, "mute": MUTE}
        defs = ["<defs>"]
        for k, c in colors.items():
            defs.append(
                f'<marker id="ah-{k}" viewBox="0 0 10 10" refX="9.2" refY="5" '
                f'markerWidth="3.1" markerHeight="3.1" orient="auto" '
                f'markerUnits="userSpaceOnUse">'
                f'<path d="M0.5,1 L9.5,5 L0.5,9 L2.4,5 z" fill="{c}"/></marker>')
        defs.append("</defs>")
        head = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" '
                f'shape-rendering="geometricPrecision" text-rendering="geometricPrecision">')
        bg = f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>'
        return "\n".join([head] + defs + [bg] + self.parts + ["</svg>"]) + "\n"


def color_key(c):
    return {BLUE: "blue", GREEN: "green", ORANGE: "orange", VERM: "verm",
            PURPLE: "purple", SKY: "sky", LINE: "line", MUTE: "mute"}.get(c, "line")


# ---------------------------------------------------------------- 文案
EN = dict(
    pool="Vitamin B6 pool\nin the TME\n(PL · PN · PM)",
    uptake="SLC19A3",
    cell="SPP1⁺ TAM  (PDXK high)",
    pl="PL", plp="PLP", pdxk="PDXK",
    drug1="4-DP / P57",
    kyn_title="PLP-dependent\nTrp catabolism",
    kyn_body="Trp → Kyn\nKYNU · KAT\n→ AHR ligands",
    nucleus="Nucleus",
    rip="RIP140",
    rip_sub="PLP–Lys613 adduct",
    rip_mod="corepressor\nreprogramming",
    ppar="PPARγ", rxr="RXR", ppre="PPRE",
    act="transactivation ↑",
    genes=["ARG1", "TGFB1", "CD36", "SPP1"],
    gene_cap="immunosuppressive transcriptional programme of the SPP1⁺ state",
    drug2="GW9662",
    spp1="SPP1",
    treg_t="CD137⁺ Treg induction & recruitment",
    treg_b="SPP1–CD44–NF-κB1 → TNFRSF9\nTGF-β1 · IL-10 · PD-L1\nKyn–AHR signalling",
    tnk_t="CD8⁺ T and NK cell dysfunction",
    tnk_b="PLP ↓ → p70S6K → BACH2-P\nloss of stemness → exhaustion\nimpaired NK glycogenolysis",
    out="Primary resistance\nto anti-PD-1 therapy",
    deprive="local vitamin B6 deprivation",
    legend=("therapeutic intervention:  PDXK (4-DP / P57, myeloid-restricted)  ·  "
            "PPARγ (GW9662)  ·  SPP1–CD44 (LNP-siSPP1, anti-CD44)"),
    legend2="PPARγ-driven SPP1 transcription reinforces the SPP1⁺ state (feed-forward loop)",
)

CN = dict(
    pool="微环境中的\n维生素 B6 池\n(PL · PN · PM)",
    uptake="SLC19A3 摄取",
    cell="SPP1⁺ 巨噬细胞（PDXK 高表达）",
    pl="PL", plp="PLP", pdxk="PDXK",
    drug1="4-DP / P57",
    kyn_title="PLP 依赖的\n色氨酸分解",
    kyn_body="Trp → Kyn\nKYNU · KAT\n→ AHR 配体",
    nucleus="细胞核",
    rip="RIP140",
    rip_sub="PLP–Lys613 加合",
    rip_mod="共调节因子\n重编程",
    ppar="PPARγ", rxr="RXR", ppre="PPRE",
    act="转录活性 ↑",
    genes=["ARG1", "TGFB1", "CD36", "SPP1"],
    gene_cap="维持 SPP1⁺ 表型的免疫抑制转录程序",
    drug2="GW9662",
    spp1="SPP1",
    treg_t="CD137⁺ Treg 诱导与招募",
    treg_b="SPP1–CD44–NF-κB1 → TNFRSF9\nTGF-β1 · IL-10 · PD-L1\nKyn–AHR 信号",
    tnk_t="CD8⁺ T 与 NK 细胞功能障碍",
    tnk_b="PLP ↓ → p70S6K → BACH2 磷酸化\n干性丧失 → 耗竭\nNK 糖原分解受损",
    out="抗 PD-1 治疗\n原发耐药",
    deprive="微环境局部维生素 B6 剥夺",
    legend=("干预靶点：PDXK（4-DP / P57，髓系限定）  ·  "
            "PPARγ（GW9662）  ·  SPP1–CD44（LNP-siSPP1、anti-CD44）"),
    legend2="PPARγ 直接转录 SPP1，形成强化 SPP1⁺ 表型的正反馈环路",
)


def build(t, font):
    s = Svg(font)

    # ---------------- 左：TME 维生素 B6 池 ----------------
    s.rect(4, 10, 26, 24, r=3, fill=BLUE, fill_opacity=0.10, stroke=BLUE, sw=0.5)
    s.text(17, 18.5, t["pool"], size=5.6, weight="bold", fill=BLUE, spacing=6.2)

    # 摄取箭头
    s.arrow(30.5, 22, 43.2, 22, color=BLUE, sw=0.75)
    s.text(37, 19.4, t["uptake"], size=4.8, fill=BLUE)

    # ---------------- 中：SPP1+ TAM 细胞 ----------------
    s.rect(44, 6, 68, 80, r=11, fill="#F7F9F8", fill_opacity=1.0, stroke=LINE, sw=0.7)
    s.text(48, 12.2, t["cell"], size=6.4, anchor="start", weight="bold", fill=INK)

    # PL -> PLP
    s.circle(55, 22, 4.6, "#FFFFFF", stroke=BLUE, sw=0.55)
    s.text(55, 23.4, t["pl"], size=5.6, weight="bold", fill=BLUE)
    s.arrow(60.4, 22, 73.2, 22, color=BLUE, sw=0.75)
    s.text(67, 19.2, t["pdxk"], size=5.4, weight="bold", fill=BLUE)
    s.circle(79.5, 22, 5.6, BLUE, stroke=None)
    s.text(79.5, 23.6, t["plp"], size=5.8, weight="bold", fill="#FFFFFF")
    # 抑制符号（PDXK）
    s.inhibit(67, 22, angle=90, length=5.0)
    s.text(67, 29.6, t["drug1"], size=4.8, fill=VERM, weight="bold")

    # 犬尿氨酸通路
    s.rect(90, 14, 20, 21, r=2.4, fill=PURPLE, fill_opacity=0.09, stroke=PURPLE, sw=0.4)
    s.text(100, 18.0, t["kyn_title"], size=4.4, fill=PURPLE, weight="bold", spacing=4.8)
    s.text(100, 26.0, t["kyn_body"], size=4.8, fill=INK, spacing=5.1)
    s.arrow(85.4, 23, 89.2, 23, color=PURPLE, sw=0.5)

    # PLP -> 核
    s.line(79.5, 28, 79.5, 38.4, stroke=BLUE, sw=0.7)

    # ---------------- 细胞核 ----------------
    s.rect(48, 38, 60, 44, r=4.5, fill=GREEN, fill_opacity=0.07, stroke=GREEN, sw=0.5)
    s.text(51, 42.4, t["nucleus"], size=4.6, anchor="start", fill=MUTE, style="italic")

    # RIP140
    s.rect(50.5, 44.5, 19, 9, r=2, fill="#FFFFFF", stroke=MUTE, sw=0.4)
    s.text(60, 48.2, t["rip"], size=5.2, weight="bold", fill=INK)
    s.text(60, 51.9, t["rip_sub"], size=4.2, fill=MUTE)
    s.path("M 78.6,39.8 Q 72.5,41.2 70.2,44.1", color=BLUE, sw=0.5)
    s.path("M 60,53.6 Q 60,57.6 68.2,57.6", color=MUTE, sw=0.45, dash="1.2 1.0")
    s.text(50.8, 61.0, t["rip_mod"], size=4.2, fill=MUTE, style="italic",
           anchor="start", spacing=4.6)

    # PPARγ : RXR 与 PPRE
    s.line(68, 64.6, 94, 64.6, stroke=INK, sw=0.5)
    s.line(68, 65.7, 94, 65.7, stroke=INK, sw=0.5)
    s.rect(73.5, 63.7, 12, 3, r=0.6, fill=GREEN, fill_opacity=0.28, stroke=GREEN, sw=0.35)
    s.text(89.6, 69.4, t["ppre"], size=4.0, fill=GREEN, anchor="start")
    s.line(85.5, 65.2, 88.8, 68.2, stroke=GREEN, sw=0.3)
    s.ellipse(76, 57.6, 7.2, 4.6, GREEN)
    s.text(76, 59.2, t["ppar"], size=5.4, weight="bold", fill="#FFFFFF")
    s.ellipse(88.5, 57.6, 5.4, 4.6, "#8FBFAE")
    s.text(88.5, 59.2, t["rxr"], size=4.8, weight="bold", fill="#FFFFFF")
    s.arrow(79.4, 39.2, 77.3, 52.6, color=BLUE, sw=0.7)
    s.text(95.4, 43.6, t["act"], size=4.4, fill=BLUE, anchor="start",
           style="italic", spacing=4.8)

    # 抑制符号（PPARγ）
    s.line(88.5, 51.4, 82.6, 53.4, stroke=VERM, sw=0.5)
    s.inhibit(82.0, 53.6, angle=70, length=4.2)
    s.text(99.6, 50.4, t["drug2"], size=4.8, fill=VERM, weight="bold", anchor="end")

    # 靶基因
    gene_boxes = [(50.5, 13.5), (65.5, 14.5), (81.5, 10.5), (93.0, 12.0)]
    s.line(57.2, 71.4, 99, 71.4, stroke=INK, sw=0.4)
    s.line(79.5, 66.7, 79.5, 71.4, stroke=INK, sw=0.4)
    for i, (gx, gw) in enumerate(gene_boxes):
        cx = gx + gw / 2
        last = (i == len(gene_boxes) - 1)
        col = ORANGE if last else INK
        s.line(cx, 71.4, cx, 73.0, stroke=INK, sw=0.4)
        s.rect(gx, 73.2, gw, 7.0, r=1.6,
               fill=ORANGE if last else "#FFFFFF",
               fill_opacity=0.18 if last else 1.0,
               stroke=col, sw=0.5 if last else 0.4)
        s.text(cx, 78.0, t["genes"][i], size=5.2, weight="bold", fill=col)
    s.text(78, 90.2, t["gene_cap"], size=4.4, fill=MUTE, style="italic")

    # 正反馈：SPP1 -> PPARγ
    s.path("M 100,72.9 Q 106.5,67.5 94.4,60.4", color=ORANGE, sw=0.55, dash="1.6 1.1")
    s.circle(104.0, 66.6, 1.9, "#FFFFFF", stroke=ORANGE, sw=0.45)
    s.text(104.0, 68.1, "+", size=5.6, weight="bold", fill=ORANGE)

    # ---------------- SPP1 分泌 ----------------
    s.path("M 105.2,76.4 Q 118.5,71 121,43.0", color=ORANGE, sw=0.8)
    s.rect(112.5, 34.4, 17, 8.4, r=4.2, fill=ORANGE, fill_opacity=0.22,
           stroke=ORANGE, sw=0.55)
    s.text(121, 39.6, t["spp1"], size=5.4, weight="bold", fill="#8A5F00")

    # ---------------- 右：Treg ----------------
    s.rect(130, 8, 46, 34, r=3, fill=PURPLE, fill_opacity=0.10, stroke=PURPLE, sw=0.55)
    s.text(153, 15.0, t["treg_t"], size=5.8, weight="bold", fill="#A34C86", spacing=6.4)
    s.text(153, 24.5, t["treg_b"], size=4.8, fill=INK, spacing=5.6)

    # SPP1 -> Treg，AHR 配体 -> Treg
    s.path("M 121,34.0 Q 123.5,28 128.8,25.6", color=ORANGE, sw=0.7)
    s.inhibit(124.2, 28.6, angle=28, length=4.2)
    s.path("M 110.4,22 Q 121,19.5 128.8,18.4", color=PURPLE, sw=0.6)

    # ---------------- 右：CD8 T / NK ----------------
    s.rect(130, 72, 46, 32, r=3, fill=SKY, fill_opacity=0.13, stroke=SKY, sw=0.55)
    s.text(153, 79.0, t["tnk_t"], size=5.8, weight="bold", fill="#1E7BA8", spacing=6.4)
    s.text(153, 87.6, t["tnk_b"], size=4.8, fill=INK, spacing=5.6)
    s.path("M 121,43.0 Q 116,62 128.6,76.5", color=ORANGE, sw=0.7)

    # 局部 B6 剥夺
    s.path("M 17,34.6 L 17,96 L 128.6,96", color=BLUE, sw=0.6, dash="2.2 1.4")
    s.text(72, 94.2, t["deprive"], size=4.8, fill=BLUE, style="italic")

    # ---------------- 右：结局 ----------------
    s.rect(130, 48, 46, 18, r=3, fill=VERM, fill_opacity=0.14, stroke=VERM, sw=0.75)
    s.text(153, 55.6, t["out"], size=6.4, weight="bold", fill="#A34600", spacing=7.0)
    s.arrow(153, 42.6, 153, 47.2, color=PURPLE, sw=0.7)
    s.arrow(153, 71.4, 153, 66.8, color=SKY, sw=0.7)

    # ---------------- 图例 ----------------
    # 符号用图形绘制，避免 ⊣ / ⊕ 在嵌入字体的 PDF 中缺字
    s.line(4.2, 101.0, 7.0, 101.0, stroke=VERM, sw=0.5)
    s.inhibit(7.2, 101.0, angle=90, length=2.8, sw=0.6)
    s.text(9.8, 102.4, t["legend"], size=4.6, anchor="start", fill=MUTE)
    s.circle(6.0, 105.2, 1.5, "#FFFFFF", stroke=ORANGE, sw=0.4)
    s.text(6.0, 106.4, "+", size=4.4, weight="bold", fill=ORANGE)
    s.text(9.8, 106.6, t["legend2"], size=4.6, anchor="start", fill=MUTE)

    return s.render()


def main():
    for tag, txt, font in (("EN", EN, FONT_EN), ("CN", CN, FONT_CN)):
        out = OUT_DIR / f"mechanism_VB6_SPP1_TAM_{tag}.svg"
        out.write_text(build(txt, font), encoding="utf-8")
        print(f"wrote {out}  ({out.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
