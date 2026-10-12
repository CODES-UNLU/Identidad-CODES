"""Genera el logo de CODES++ vectorizado con la paleta de codesunlu.tech.

Uso: python generar_logo.py
Salida: svg/logo.svg (adaptable claro/oscuro), svg/logo-claro.svg,
        svg/logo-oscuro.svg, svg/logo-mono.svg
"""
import math
from pathlib import Path

# Paleta del sitio (variables CSS de codesunlu.tech)
PRIMARY = "#39c0c3"        # --primary / --accent / theme-color
PRIMARY_LIGHT = "#5dd5d8"  # --primary-light
PRIMARY_DARK = "#2a8a8d"   # --primary-dark / --accent-hover
PRIMARY_DEEP = "#1e6b6e"   # tono profundo usado en el sitio

# Variantes: (inicio degradado, fin degradado, brillo de la C)
VARIANTES = {
    # Para fondos claros: tonos más oscuros para tener contraste sobre blanco
    "claro": (PRIMARY_DARK, PRIMARY_DEEP, PRIMARY),
    # Para fondos oscuros: tonos claros sobre #0f0f0f
    "oscuro": (PRIMARY_LIGHT, PRIMARY, "#9be7e9"),
}

W, H = 330, 290
STROKE = 7

GLOBE_C = (158, 148)
GLOBE_R = 116
C_C = (244, 150)
C_R = 64          # radio del eje del trazo de la C
C_W = 30          # grosor de la C
C_OPEN = 44       # medio ángulo de apertura de la C (grados)
GAP = 7           # separación entre la C y el globo


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def ellipse_pt(cx, cy, rx, ry, rot_deg, t_deg):
    t, r = math.radians(t_deg), math.radians(rot_deg)
    x, y = rx * math.cos(t), ry * math.sin(t)
    return (cx + x * math.cos(r) - y * math.sin(r),
            cy + x * math.sin(r) + y * math.cos(r))


def ellipse_arc(cx, cy, rx, ry, rot, t0, t1, steps=96, stop_in=None):
    pts = [ellipse_pt(cx, cy, rx, ry, rot, t0 + (t1 - t0) * i / steps)
           for i in range(steps + 1)]
    if stop_in:  # corta el arco en cuanto entra bajo la C (queda oculto por la máscara)
        (sx, sy), sr = stop_in
        for i, (x, y) in enumerate(pts):
            if math.hypot(x - sx, y - sy) < sr:
                pts = pts[:i + 1]
                break
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts), pts[0], pts[-1]


def circle_arc(cx, cy, r, a0, a1):
    """Arco circular de a0 a a1 grados (sentido horario en pantalla)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{f(x0)} {f(y0)} A{f(r)} {f(r)} 0 {large} 1 {f(x1)} {f(y1)}"


def node(x, y, r=8):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" stroke-width="5"/>'


def build_body():
    gx, gy = GLOBE_C
    cx, cy = C_C

    # --- Globo: contorno, meridianos y paralelos (recortados al círculo) ---
    globe = [
        f'<circle cx="{gx}" cy="{gy}" r="{GLOBE_R}"/>',
        f'<line x1="{gx}" y1="{gy - GLOBE_R}" x2="{gx}" y2="{gy + GLOBE_R}"/>',
        f'<ellipse cx="{gx}" cy="{gy}" rx="48" ry="{GLOBE_R}"/>',
        f'<ellipse cx="{gx}" cy="{gy}" rx="88" ry="{GLOBE_R}"/>',
    ]
    parallels = [
        f'<line x1="{gx - GLOBE_R}" y1="{gy}" x2="{gx + GLOBE_R}" y2="{gy}"/>',
        f'<path d="M{gx - GLOBE_R} {gy - 66} Q{gx} {gy - 44} {gx + GLOBE_R} {gy - 66}"/>',
        f'<path d="M{gx - GLOBE_R} {gy + 62} Q{gx} {gy + 84} {gx + GLOBE_R} {gy + 62}"/>',
    ]

    # --- Órbitas con nodos de circuito en los extremos ---
    hide = ((cx, cy), C_R + C_W / 2)
    o1, o1_start, _ = ellipse_arc(gx, gy, 150, 56, 36, 180, 360, stop_in=hide)
    o2, o2_start, _ = ellipse_arc(gx, gy, 150, 56, -36, 180, 0, stop_in=hide)
    orbits = [f'<path d="{o1}"/>', f'<path d="{o2}"/>']

    # Traza de circuito superior: sale del borde del globo hacia un nodo
    a = math.radians(-72)
    tx, ty = gx + GLOBE_R * math.cos(a), gy + GLOBE_R * math.sin(a)
    trace_end = (tx + 6, ty + 22)
    traces = [f'<line x1="{f(tx)}" y1="{f(ty)}" x2="{f(trace_end[0])}" y2="{f(trace_end[1])}"/>']

    nodes = [node(*o1_start), node(*o2_start), node(*trace_end)]

    # Máscara: el globo y las órbitas se cortan alrededor de la C
    mask_r = C_R + C_W / 2 + GAP
    mask = (
        '<mask id="corte" maskUnits="userSpaceOnUse" x="0" y="0" '
        f'width="{W}" height="{H}">'
        f'<rect width="{W}" height="{H}" fill="#fff"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{f(mask_r)}" fill="#000"/>'
        '</mask>'
        f'<clipPath id="globo"><circle cx="{gx}" cy="{gy}" r="{GLOBE_R}"/></clipPath>'
    )

    # --- La C ---
    c_main = circle_arc(cx, cy, C_R, C_OPEN, 360 - C_OPEN)
    c_shine = circle_arc(cx, cy, C_R - C_W / 2 + 6, C_OPEN + 14, 300)
    # Nodo de circuito dentro de la C
    inner_node = (cx + 11, cy + 15)
    inner_trace = f'<line x1="{cx - 16}" y1="{cy + 30}" x2="{f(inner_node[0])}" y2="{f(inner_node[1])}"/>'

    lines_attr = (f'fill="none" stroke="url(#trazo)" stroke-width="{STROKE}" '
                  'stroke-linecap="round" stroke-linejoin="round"')
    return mask, f"""
  <g mask="url(#corte)" {lines_attr}>
    {"".join(globe)}
    <g clip-path="url(#globo)">{"".join(parallels)}</g>
    {"".join(orbits)}
    {"".join(traces)}
    <g>{"".join(nodes)}</g>
  </g>
  <path class="c" d="{c_main}" fill="none" stroke="url(#letra)" stroke-width="{C_W}"/>
  <path class="brillo" d="{c_shine}" fill="none" stroke-width="5" stroke-linecap="round"/>
  <g {lines_attr}>
    {inner_trace}
    <g>{node(*inner_node, 7)}</g>
  </g>"""


def gradients(c0, c1):
    return (
        f'<linearGradient id="trazo" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">'
        f'<stop offset="0" class="s0" stop-color="{c0}"/><stop offset="1" class="s1" stop-color="{c1}"/>'
        f'</linearGradient>'
        f'<linearGradient id="letra" gradientUnits="userSpaceOnUse" x1="0" y1="{C_C[1] - C_R - C_W}" x2="0" y2="{C_C[1] + C_R + C_W}">'
        f'<stop offset="0" class="s0" stop-color="{c0}"/><stop offset="1" class="s1" stop-color="{c1}"/>'
        f'</linearGradient>'
    )


def svg(defs, body, style="", title="CODES++"):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">{title}</title>{style}
  <defs>{defs}</defs>{body}
</svg>
"""


def main():
    out = Path(__file__).parent / "svg"
    out.mkdir(exist_ok=True)
    mask, body = build_body()

    for name, (c0, c1, shine) in VARIANTES.items():
        style = f"<style>.brillo{{stroke:{shine};opacity:.55}}</style>"
        (out / f"logo-{name}.svg").write_text(
            svg(mask + gradients(c0, c1), body, style), encoding="utf-8")

    # Adaptable: sigue el modo claro/oscuro del sistema (también dentro de <img>)
    lc0, lc1, lsh = VARIANTES["claro"]
    dc0, dc1, dsh = VARIANTES["oscuro"]
    style = (
        "<style>"
        f".s0{{stop-color:{lc0}}}.s1{{stop-color:{lc1}}}.brillo{{stroke:{lsh};opacity:.55}}"
        "@media (prefers-color-scheme:dark){"
        f".s0{{stop-color:{dc0}}}.s1{{stop-color:{dc1}}}.brillo{{stroke:{dsh}}}"
        "}</style>"
    )
    (out / "logo.svg").write_text(svg(mask + gradients(lc0, lc1), body, style), encoding="utf-8")

    # Monocromo: toma el color del texto donde se inserte (currentColor)
    mono_body = (body.replace("url(#trazo)", "currentColor")
                     .replace("url(#letra)", "currentColor"))
    style = "<style>.brillo{stroke:none}</style>"
    (out / "logo-mono.svg").write_text(
        svg(mask, mono_body, style).replace("<svg ", '<svg fill="none" color="#39c0c3" ', 1),
        encoding="utf-8")
    print("SVG generados en", out)


if __name__ == "__main__":
    main()
