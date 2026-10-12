"""Genera el logo de CODES++ vectorizado con la paleta de codesunlu.tech.

Uso: python generar_logo.py
Salida: svg/logo.svg (adaptable claro/oscuro), svg/logo-claro.svg,
        svg/logo-oscuro.svg, svg/logo-mono.svg y png/*.png (si hay resvg_py)

Intercala colores como el wordmark del sitio (teal + tinta):
  - teal: contorno del globo, paralelos y mitad superior de la C
  - cian: órbitas y nodos de circuito
  - tinta: meridianos y mitad inferior de la C (#2c3e50 en claro, #e9ecef en oscuro)
"""
import math
from pathlib import Path

# Paleta del sitio (CSS de codesunlu.tech). Cada tema define todos los roles.
TEMAS = {
    # Para fondos claros: tonos con contraste sobre blanco
    "claro": {
        "teal0": "#39c0c3",   # --primary
        "teal1": "#1e6b6e",   # teal profundo
        "cian0": "#00b8e0",   # #00d4ff oscurecido para leer sobre blanco
        "cian1": "#2a8a8d",   # --primary-dark
        "tinta": "#2c3e50",
        "brillo": "#5dd5d8",  # --primary-light
    },
    # Para fondos oscuros (#0f0f0f del sitio)
    "oscuro": {
        "teal0": "#5dd5d8",   # --primary-light
        "teal1": "#2a8a8d",   # --primary-dark
        "cian0": "#00d4ff",
        "cian1": "#39c0c3",   # --primary
        "tinta": "#e9ecef",
        "brillo": "#b8f0f1",
    },
}

W, H = 340, 300

GLOBE_C = (160, 152)
GLOBE_R = 118
C_C = (250, 154)
C_R = 64          # radio del eje del trazo de la C
C_W = 32          # grosor de la C
C_OPEN = 42       # medio ángulo de apertura de la C (grados)
GAP = 6           # separación alrededor de la C y en los cruces de las órbitas

W_CONTORNO = 9    # contorno del globo
W_RED = 5         # meridianos y paralelos
W_ORBITA = 6.5    # órbitas y trazas
NODE_R = 8.5      # radio de los anillos de nodo


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def ellipse_pt(cx, cy, rx, ry, rot_deg, t_deg):
    t, r = math.radians(t_deg), math.radians(rot_deg)
    x, y = rx * math.cos(t), ry * math.sin(t)
    return (cx + x * math.cos(r) - y * math.sin(r),
            cy + x * math.sin(r) + y * math.cos(r))


def ellipse_arc(cx, cy, rx, ry, rot, t0, t1, steps=120, stop_in=None):
    pts = [ellipse_pt(cx, cy, rx, ry, rot, t0 + (t1 - t0) * i / steps)
           for i in range(steps + 1)]
    if stop_in:  # corta el arco en cuanto entra bajo la C (queda oculto por la máscara)
        (sx, sy), sr = stop_in
        for i, (x, y) in enumerate(pts):
            if math.hypot(x - sx, y - sy) < sr:
                pts = pts[:i + 1]
                break
    start = pts[0]  # ahí va el nodo: el trazo arranca en el borde del anillo
    pts = [p for p in pts if math.hypot(p[0] - start[0], p[1] - start[1]) >= NODE_R]
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts), start


def circle_arc(cx, cy, r, a0, a1):
    """Arco circular de a0 a a1 grados (sentido horario en pantalla)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{f(x0)} {f(y0)} A{f(r)} {f(r)} 0 {large} 1 {f(x1)} {f(y1)}"


def node(x, y):
    """Nodo de circuito: anillo con punto central."""
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{NODE_R}" class="anillo"/>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="3" class="punto"/>')


def build():
    gx, gy = GLOBE_C
    cx, cy = C_C
    corte_c = C_R + C_W / 2 + GAP

    # --- Órbitas (pasan por delante del globo) ---
    hide = ((cx, cy), C_R + C_W / 2)
    o1, o1_start = ellipse_arc(gx, gy, 154, 58, 36, 180, 360, stop_in=hide)
    o2, o2_start = ellipse_arc(gx, gy, 154, 58, -36, 180, 0, stop_in=hide)

    # Traza superior: del contorno del globo hacia un nodo interior
    a = math.radians(-72)
    tx, ty = gx + GLOBE_R * math.cos(a), gy + GLOBE_R * math.sin(a)
    top_node = (tx + 6, ty + 24)
    top_trace = f"M{f(tx)} {f(ty)} L{f(top_node[0])} {f(top_node[1] - NODE_R)}"

    # Nodo dentro de la C
    inner_node = (cx + 12, cy + 14)
    inner_trace = f"M{cx - 18} {cy + 32} L{f(inner_node[0] - 6.5)} {f(inner_node[1] + 4)}"

    orbit_paths = [o1, o2]
    nodes = [o1_start, o2_start]

    # --- Máscaras ---
    gap_paths = "".join(
        f'<path d="{d}" stroke-width="{W_ORBITA + 2 * GAP}"/>' for d in orbit_paths)
    gap_nodes = "".join(
        f'<circle cx="{f(x)}" cy="{f(y)}" r="{NODE_R + W_ORBITA / 2 + GAP}"/>' for x, y in nodes)
    defs = f"""
    <clipPath id="globo"><circle cx="{gx}" cy="{gy}" r="{GLOBE_R}"/></clipPath>
    <mask id="cortaC" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <rect width="{W}" height="{H}" fill="#fff"/>
      <circle cx="{cx}" cy="{cy}" r="{f(corte_c)}"/>
    </mask>
    <mask id="cortaGlobo" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <rect width="{W}" height="{H}" fill="#fff"/>
      <g fill="none" stroke="#000" stroke-linecap="round">{gap_paths}</g>
      {gap_nodes}
      <circle cx="{cx}" cy="{cy}" r="{f(corte_c)}"/>
    </mask>
    <linearGradient id="gTeal" gradientUnits="userSpaceOnUse" x1="{gx - GLOBE_R}" y1="{gy - GLOBE_R}" x2="{gx + GLOBE_R}" y2="{gy + GLOBE_R}">
      <stop offset="0" class="teal0"/><stop offset="1" class="teal1"/>
    </linearGradient>
    <linearGradient id="gCian" gradientUnits="userSpaceOnUse" x1="0" y1="{gy - 90}" x2="{W}" y2="{gy + 90}">
      <stop offset="0" class="cian0"/><stop offset="1" class="cian1"/>
    </linearGradient>
    <linearGradient id="gLetra" gradientUnits="userSpaceOnUse" x1="{cx}" y1="{cy - C_R - C_W / 2}" x2="{cx}" y2="{cy}">
      <stop offset="0" class="teal0"/><stop offset="1" class="teal1"/>
    </linearGradient>"""

    # --- Globo ---
    mer = (f'<line x1="{gx}" y1="{gy - GLOBE_R}" x2="{gx}" y2="{gy + GLOBE_R}"/>'
           f'<ellipse cx="{gx}" cy="{gy}" rx="50" ry="{GLOBE_R}"/>'
           f'<ellipse cx="{gx}" cy="{gy}" rx="90" ry="{GLOBE_R}"/>')
    par = (f'<line x1="{gx - GLOBE_R}" y1="{gy}" x2="{gx + GLOBE_R}" y2="{gy}"/>'
           f'<path d="M{gx - GLOBE_R} {gy - 70} Q{gx} {gy - 46} {gx + GLOBE_R} {gy - 70}"/>'
           f'<path d="M{gx - GLOBE_R} {gy + 66} Q{gx} {gy + 90} {gx + GLOBE_R} {gy + 66}"/>')

    # --- La C, en dos tonos como la "S" del wordmark ---
    split = 182
    c_top = circle_arc(cx, cy, C_R, split + 2, 360 - C_OPEN)
    c_bottom = circle_arc(cx, cy, C_R, C_OPEN, split - 2)
    c_shine = circle_arc(cx, cy, C_R - C_W / 2 + 5, split + 14, 360 - C_OPEN - 12)

    body = f"""
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <g mask="url(#cortaGlobo)">
      <g clip-path="url(#globo)">
        <g class="tinta" stroke-width="{W_RED}">{mer}</g>
        <g stroke="url(#gTeal)" stroke-width="{W_RED}">{par}</g>
      </g>
      <circle cx="{gx}" cy="{gy}" r="{GLOBE_R}" stroke="url(#gTeal)" stroke-width="{W_CONTORNO}"/>
      <path d="{top_trace}" stroke="url(#gCian)" stroke-width="{W_ORBITA}"/>
    </g>
    <g mask="url(#cortaC)" stroke="url(#gCian)" stroke-width="{W_ORBITA}">
      {"".join(f'<path d="{d}"/>' for d in orbit_paths)}
    </g>
    <path d="{c_top}" stroke="url(#gLetra)" stroke-width="{C_W}" stroke-linecap="butt"/>
    <path d="{c_bottom}" class="tinta" stroke-width="{C_W}" stroke-linecap="butt"/>
    <path d="{c_shine}" class="brillo" stroke-width="4"/>
    <path d="{inner_trace}" stroke="url(#gCian)" stroke-width="{W_ORBITA}"/>
    <g stroke="url(#gCian)" stroke-width="{W_ORBITA - 1.5}">
      {"".join(node(*p) for p in nodes + [top_node, inner_node])}
    </g>
  </g>"""
    return defs, body


def css(t):
    return (f".teal0{{stop-color:{t['teal0']}}}.teal1{{stop-color:{t['teal1']}}}"
            f".cian0{{stop-color:{t['cian0']}}}.cian1{{stop-color:{t['cian1']}}}"
            f".tinta{{stroke:{t['tinta']}}}.brillo{{stroke:{t['brillo']};opacity:.6}}"
            f".punto{{fill:{t['cian0']};stroke:none}}")


def svg(style, defs, body, extra=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t"{extra}>
  <title id="t">CODES++</title>
  <style>{style}</style>
  <defs>{defs}
  </defs>{body}
</svg>
"""


def main():
    root = Path(__file__).parent
    out = root / "svg"
    out.mkdir(exist_ok=True)
    defs, body = build()

    for name, tema in TEMAS.items():
        (out / f"logo-{name}.svg").write_text(svg(css(tema), defs, body), encoding="utf-8")

    # Adaptable: sigue el modo claro/oscuro del sistema (también dentro de <img>)
    style = css(TEMAS["claro"]) + "@media (prefers-color-scheme:dark){" + css(TEMAS["oscuro"]) + "}"
    (out / "logo.svg").write_text(svg(style, defs, body), encoding="utf-8")

    # Monocromo: todo en currentColor (un solo color donde se inserte)
    mono_defs = defs
    for stop in ("teal0", "teal1", "cian0", "cian1"):
        mono_defs = mono_defs.replace(f'class="{stop}"', 'stop-color="currentColor"')
    mono_style = ".tinta{stroke:currentColor}.brillo{stroke:none}.punto{fill:currentColor;stroke:none}"
    (out / "logo-mono.svg").write_text(
        svg(mono_style, mono_defs, body, ' color="#39c0c3"'), encoding="utf-8")

    try:
        import resvg_py
    except ImportError:
        print("resvg_py no instalado: se omiten los PNG")
    else:
        png = root / "png"
        png.mkdir(exist_ok=True)
        for name in TEMAS:
            for w in (512, 1024, 2048):
                data = resvg_py.svg_to_bytes(svg_path=str(out / f"logo-{name}.svg"),
                                             width=w, height=round(w * H / W))
                (png / f"logo-{name}-{w}.png").write_bytes(bytes(data))
    print("Logo generado en", out)


if __name__ == "__main__":
    main()
