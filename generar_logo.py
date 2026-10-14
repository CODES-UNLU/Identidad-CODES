"""Genera el logo de CODES++ vectorizado.

Uso: python generar_logo.py
Salida: svg/logo.svg (adaptable claro/oscuro), svg/logo-claro.svg, svg/logo-oscuro.svg,
        svg/logo-mono.svg y, si está instalado resvg_py, los PNG de png/

Composición: un globo terráqueo que emerge de un libro abierto (las páginas bajan
en V hasta el lomo), con la C de CODES al frente, apoyada sobre la página
derecha, y un nodo de circuito dentro de la C.

Paleta: una sola familia teal, de tono constante (OKLCH h ≈ 197.6°) y anclada en
los colores del sitio codesunlu.tech (300 = --primary-light, 400 = --primary,
600 = --primary-dark). Cada capa usa su propio escalón:
  - grilla: meridianos y paralelos, la capa más tenue
  - trazo:  contorno del globo, libro y nodo (degradado a 135°, como el sitio)
  - letra:  la C, la capa de mayor contraste con el fondo
"""
import bisect
import math
from pathlib import Path

# Escala tonal: pasos parejos de luminosidad OKLCH con el mismo tono
ESCALA = {
    50: "#e7fafa",
    100: "#c8f3f4",
    200: "#95e7e8",
    300: "#5dd5d8",  # --primary-light
    400: "#39c0c3",  # --primary
    500: "#30a5a8",
    600: "#2a8a8d",  # --primary-dark
    700: "#1d6d6f",
    800: "#125355",
    900: "#083b3c",
    950: "#022324",
}

# Escalón de ESCALA para cada rol; los degradados van de (inicio, fin) a 135°
TEMAS = {
    # Fondo claro: cuanto más importante el elemento, más profundo el tono
    "claro": {"grilla": 300, "trazo": (400, 600), "letra": (500, 700), "punto": 700},
    # Fondo oscuro (#0f0f0f del sitio): cuanto más importante, más luminoso
    "oscuro": {"grilla": 700, "trazo": (300, 500), "letra": (200, 400), "punto": 50},
}
FONDO_AVATAR = "#0f0f0f"  # --background del sitio
AVATAR_ANCHO = 0.74       # ancho del logo dentro del avatar cuadrado

# --- Geometría (unidades del viewBox; casi todo se mide en radios del globo) ---
R = 118            # radio del globo
MARGEN = 12        # aire alrededor del dibujo
GAP = 6            # separación en los cruces
W_CONTORNO = 9
W_GRILLA = 5
W_LIBRO = 7.5
W_TRAZA = 6.5
MIN_TRAMO = 34     # los tramos de grilla más cortos se quitan: no quedan fragmentos sueltos

MERIDIANOS = (0.42, 0.76)                         # semieje horizontal de cada meridiano
PARALELOS = ((-0.59, 0.18), (0, 0), (0.42, 0.18))  # (altura, comba)

# Libro abierto: dos páginas por lado que bajan en V hasta el lomo
LIBRO_ANCHO = 1.28   # mitad del ancho
LIBRO_LOMO = 1.0     # altura del lomo bajo el centro del globo (lo toca por abajo)
LIBRO_ALZA = 0.58    # cuánto suben las puntas respecto del lomo
LIBRO_CAIDA = 0.06   # leve caída de las puntas de página
PAGINAS = 2
PAGINA_DY = 14       # separación entre páginas en la punta
PAGINA_DG = 8        # y en el lomo

# La C, a la derecha del globo; su altura se calcula para que apoye sobre la página
C_DX = 0.74
C_R = 0.5          # radio del eje del trazo
C_W = 0.26         # grosor
C_APERTURA = 42    # medio ángulo de la abertura (grados)
C_APOYO = 8        # luz entre la C y la página derecha
NODO_POS = (0.1, 0.12)  # posición del nodo respecto del centro de la C
NODO_R = 8.5       # anillo del nodo
NODO_ANG = 31      # inclinación de la traza que une el nodo con la C (grados)


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def bezier(c, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = c
    u = 1 - t
    a, b, cc, d = u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t
    return a * x0 + b * x1 + cc * x2 + d * x3, a * y0 + b * y1 + cc * y2 + d * y3


def pagina(i, lado):
    """Borde de la página i (0 = la de arriba), del lomo a la punta. lado: -1 izquierda, 1 derecha."""
    ancho = LIBRO_ANCHO * R
    y_lomo = LIBRO_LOMO * R + i * PAGINA_DG
    y_punta = (LIBRO_LOMO - LIBRO_ALZA) * R + i * PAGINA_DY
    return ((0, y_lomo),
            (lado * 0.2 * ancho, y_lomo - 0.72 * (y_lomo - y_punta)),  # sale empinada del lomo
            (lado * 0.68 * ancho, y_punta - LIBRO_CAIDA * R),          # y se aplana hacia la punta
            (lado * ancho, y_punta))


def centro_c():
    """A C_DX del globo y a la altura justa para quedar a C_APOYO de la página derecha."""
    borde = [bezier(pagina(0, 1), i / 400) for i in range(401)]
    cx, distancia = C_DX * R, (C_R + C_W / 2) * R + W_LIBRO / 2 + C_APOYO
    arriba, abajo = -R, R
    for _ in range(50):
        cy = (arriba + abajo) / 2
        if min(math.hypot(x - cx, y - cy) for x, y in borde) > distancia:
            arriba = cy
        else:
            abajo = cy
    return cx, arriba


C_X, C_Y = centro_c()
C_EXT = (C_R + C_W / 2) * R  # radio exterior de la C


def lienzo():
    """Tamaño del viewBox y posición del centro del globo, con MARGEN parejo alrededor."""
    arriba = min(-R - W_CONTORNO / 2, C_Y - C_EXT)
    abajo = LIBRO_LOMO * R + (PAGINAS - 1) * PAGINA_DG + W_LIBRO / 2
    izq = -LIBRO_ANCHO * R - W_LIBRO / 2
    der = max(LIBRO_ANCHO * R + W_LIBRO / 2, C_X + C_EXT)
    w, h = math.ceil(der - izq + 2 * MARGEN), math.ceil(abajo - arriba + 2 * MARGEN)
    return w, h, (w - der - izq) / 2, (h - abajo - arriba) / 2


W, H, OX, OY = lienzo()


def P(x, y):
    """Punto relativo al centro del globo -> coordenadas del viewBox."""
    return f"{f(x + OX)} {f(y + OY)}"


def curva(c):
    return f"M{P(*c[0])} C{P(*c[1])} {P(*c[2])} {P(*c[3])}"


# --- Qué partes del globo quedan tapadas por la C y por el libro ---
class Recortes:
    def __init__(self):
        self.r_c = C_EXT + GAP
        self.borde = [bezier(pagina(0, lado), i / 300) for lado in (-1, 1) for i in range(301)]
        perfil = sorted(self.borde)
        self.px, self.py = [p[0] for p in perfil], [p[1] for p in perfil]
        self.y_borde = min(self.py) - W_LIBRO / 2 - GAP

    def bajo_el_libro(self, x, y):
        i = bisect.bisect_left(self.px, x)
        if i in (0, len(self.px)):
            return False
        x0, x1, y0, y1 = self.px[i - 1], self.px[i], self.py[i - 1], self.py[i]
        return y > (y0 if x1 == x0 else y0 + (y1 - y0) * (x - x0) / (x1 - x0))

    def visible(self, x, y):
        if math.hypot(x - C_X, y - C_Y) < self.r_c:
            return False
        if y > self.y_borde:
            if self.bajo_el_libro(x, y):
                return False
            if min(math.hypot(x - bx, y - by) for bx, by in self.borde) < W_LIBRO / 2 + GAP:
                return False
        return True


def tramos(muestras, recortes, ancho, solo_dentro=True):
    """Tramos visibles [(t0, t1)] de una línea muestreada [(t, (x, y))].

    Descarta los más cortos que MIN_TRAMO y estira los demás hacia la zona tapada:
    así el corte limpio lo hace la máscara y no un remate redondo.
    """
    ok = [recortes.visible(x, y) and (not solo_dentro or math.hypot(x, y) <= R)
          for _, (x, y) in muestras]
    largo = [0.0]
    for (_, a), (_, b) in zip(muestras, muestras[1:]):
        largo.append(largo[-1] + math.dist(a, b))
    res, i, n = [], 0, len(muestras)
    while i < n:
        if not ok[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and ok[j + 1]:
            j += 1
        if largo[j] - largo[i] >= MIN_TRAMO:
            a, b = i, j
            while a > 0 and largo[i] - largo[a] < ancho / 2 + 2:
                a -= 1
            while b < n - 1 and largo[b] - largo[j] < ancho / 2 + 2:
                b += 1
            res.append((muestras[a][0], muestras[b][0]))
        i = j + 1
    return res


def arco_elipse(rx, ry, t0, t1):
    """Arco de la elipse centrada en el globo, de t0 a t1 (radianes, sentido horario)."""
    a = (rx * math.cos(t0), ry * math.sin(t0))
    b = (rx * math.cos(t1), ry * math.sin(t1))
    grande = 1 if t1 - t0 > math.pi else 0
    return f"M{P(*a)} A{f(rx)} {f(ry)} 0 {grande} 1 {P(*b)}"


def elipse(rx, ry, recortes, ancho):
    # Se recorre desde el polo sur, que siempre queda dentro del libro: ningún tramo se parte
    n = 1440
    muestras = [(t, (rx * math.cos(t), ry * math.sin(t)))
                for t in (math.pi / 2 + 2 * math.pi * k / n for k in range(n + 1))]
    return [arco_elipse(rx, ry, t0, t1) for t0, t1 in tramos(muestras, recortes, ancho, solo_dentro=False)]


def paralelo(altura, comba, recortes):
    q = ((-R, altura * R), (0, (altura + comba) * R), (R, altura * R))

    def punto(t):
        u = 1 - t
        return (u * u * q[0][0] + 2 * u * t * q[1][0] + t * t * q[2][0],
                u * u * q[0][1] + 2 * u * t * q[1][1] + t * t * q[2][1])

    trazos = []
    for t0, t1 in tramos([(k / 600, punto(k / 600)) for k in range(601)], recortes, W_GRILLA):
        a, b = punto(t0), punto(t1)
        if not comba:
            trazos.append(f"M{P(*a)} L{P(*b)}")
            continue
        # Control del subtramo: a + (t1 - t0) * derivada(t0) / 2
        dx = (1 - t0) * (q[1][0] - q[0][0]) + t0 * (q[2][0] - q[1][0])
        dy = (1 - t0) * (q[1][1] - q[0][1]) + t0 * (q[2][1] - q[1][1])
        c = (a[0] + dx * (t1 - t0), a[1] + dy * (t1 - t0))
        trazos.append(f"M{P(*a)} Q{P(*c)} {P(*b)}")
    return trazos


def eje(recortes):
    """Meridiano central: baja del polo norte hasta el lomo y termina en remate redondo."""
    y = -R
    while recortes.visible(0, y + 1):
        y += 1
    return f"M{P(0, -R)} L{P(0, y - W_GRILLA / 2 - 3)}"


def arco_c(r, a0, a1):
    x0, y0 = C_X + r * math.cos(math.radians(a0)), C_Y + r * math.sin(math.radians(a0))
    x1, y1 = C_X + r * math.cos(math.radians(a1)), C_Y + r * math.sin(math.radians(a1))
    return f"M{P(x0, y0)} A{f(r)} {f(r)} 0 1 1 {P(x1, y1)}"


def geometria():
    rec = Recortes()
    grilla = [d for k in MERIDIANOS for d in elipse(k * R, R, rec, W_GRILLA)]
    grilla += [d for alt, comba in PARALELOS for d in paralelo(alt, comba, rec)]
    grilla.append(eje(rec))
    contorno = elipse(R, R, rec, W_CONTORNO)

    sup_izq, sup_der = pagina(0, -1), pagina(0, 1)
    interior = (f"M{P(*sup_izq[3])} C{P(*sup_izq[2])} {P(*sup_izq[1])} {P(*sup_izq[0])} "
                f"C{P(*sup_der[1])} {P(*sup_der[2])} {P(*sup_der[3])} "
                f"V{f(H)} H{f(sup_izq[3][0] + OX)} Z")
    libro = [curva(pagina(i, lado)) for i in range(PAGINAS) for lado in (-1, 1)]

    # Nodo dentro de la C; su traza nace en la pared interior (la C tapa el remate)
    nx, ny = C_X + NODO_POS[0] * R, C_Y + NODO_POS[1] * R
    dx, dy = -math.cos(math.radians(NODO_ANG)), math.sin(math.radians(NODO_ANG))
    ox, oy, r_int = nx - C_X, ny - C_Y, (C_R - C_W / 2) * R
    b = ox * dx + oy * dy
    t = -b + math.sqrt(b * b - (ox * ox + oy * oy - r_int * r_int)) + 3
    return {
        "grilla": grilla,
        "contorno": contorno,
        "interior": interior,
        "borde": (curva(sup_izq), curva(sup_der)),
        "libro": libro,
        "traza": f"M{P(nx + dx * t, ny + dy * t)} L{P(nx + dx * NODO_R, ny + dy * NODO_R)}",
        "c": arco_c(C_R * R, C_APERTURA, 360 - C_APERTURA),
        "nodo": (nx + OX, ny + OY),
    }


def svg(g, pinturas, estilo="", raiz=""):
    """Arma el SVG. pinturas: atributos ya formateados para cada rol."""
    p = pinturas
    gx, gy = OX, OY
    cx, cy = C_X + OX, C_Y + OY
    semi = (W + H) / 4  # degradado a 135° sobre todo el lienzo, como linear-gradient(135deg, …)
    defs = ""
    if "trazo0" in p:
        defs += (f'<linearGradient id="trazo" gradientUnits="userSpaceOnUse" x1="{f(W / 2 - semi)}" '
                 f'y1="{f(H / 2 - semi)}" x2="{f(W / 2 + semi)}" y2="{f(H / 2 + semi)}">'
                 f'<stop offset="0" {p["trazo0"]}/><stop offset="1" {p["trazo1"]}/></linearGradient>\n    '
                 f'<linearGradient id="letra" gradientUnits="userSpaceOnUse" x1="{f(cx - C_EXT)}" '
                 f'y1="{f(cy - C_EXT)}" x2="{f(cx + C_EXT)}" y2="{f(cy + C_EXT)}">'
                 f'<stop offset="0" {p["letra0"]}/><stop offset="1" {p["letra1"]}/></linearGradient>\n    ')
    nx, ny = g["nodo"]
    estilo = f"\n  <style>{estilo}</style>" if estilo else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="titulo"{raiz}>
  <title id="titulo">CODES++</title>
  <desc>Globo terráqueo que emerge de un libro abierto, con la letra C y un nodo de circuito.</desc>{estilo}
  <defs>
    {defs}<clipPath id="globo"><circle cx="{f(gx)}" cy="{f(gy)}" r="{R}"/></clipPath>
    <mask id="recorte" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <rect width="{W}" height="{H}" fill="#fff"/>
      <path d="{g["interior"]}" fill="#000"/>
      <g fill="none" stroke="#000" stroke-width="{f(W_LIBRO + 2 * GAP)}" stroke-linecap="round"><path d="{g["borde"][0]}"/><path d="{g["borde"][1]}"/></g>
      <circle cx="{f(cx)}" cy="{f(cy)}" r="{f(C_EXT + GAP)}" fill="#000"/>
    </mask>
  </defs>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <g mask="url(#recorte)">
      <g clip-path="url(#globo)" {p["grilla"]} stroke-width="{W_GRILLA}">
        {"".join(f'<path d="{d}"/>' for d in g["grilla"])}
      </g>
      <g stroke="{p["trazo"]}" stroke-width="{W_CONTORNO}">{"".join(f'<path d="{d}"/>' for d in g["contorno"])}</g>
    </g>
    <g stroke="{p["trazo"]}" stroke-width="{W_LIBRO}">
      {"".join(f'<path d="{d}"/>' for d in g["libro"])}
    </g>
    <path d="{g["traza"]}" stroke="{p["trazo"]}" stroke-width="{W_TRAZA}"/>
    <path d="{g["c"]}" stroke="{p["letra"]}" stroke-width="{f(C_W * R)}" stroke-linecap="butt"/>
    <circle cx="{f(nx)}" cy="{f(ny)}" r="{NODO_R}" stroke="{p["trazo"]}" stroke-width="5"/>
    <circle cx="{f(nx)}" cy="{f(ny)}" r="3" {p["punto"]} stroke="none"/>
  </g>
</svg>
"""


def pinturas_tema(tema):
    """Colores escritos como atributos: el SVG funciona igual en cualquier editor."""
    t = TEMAS[tema]
    return {
        "grilla": f'stroke="{ESCALA[t["grilla"]]}"',
        "punto": f'fill="{ESCALA[t["punto"]]}"',
        "trazo": "url(#trazo)", "letra": "url(#letra)",
        "trazo0": f'stop-color="{ESCALA[t["trazo"][0]]}"', "trazo1": f'stop-color="{ESCALA[t["trazo"][1]]}"',
        "letra0": f'stop-color="{ESCALA[t["letra"][0]]}"', "letra1": f'stop-color="{ESCALA[t["letra"][1]]}"',
    }


def css(tema):
    t = TEMAS[tema]
    return (f".grilla{{stroke:{ESCALA[t['grilla']]}}}.punto{{fill:{ESCALA[t['punto']]}}}"
            + "".join(f".{rol}{i}{{stop-color:{ESCALA[t[rol][i]]}}}" for rol in ("trazo", "letra") for i in (0, 1)))


def escribir(ruta, texto):
    # Siempre LF, como pide .gitattributes (en Windows write_text pondría CRLF)
    ruta.write_text(texto, encoding="utf-8", newline="\n")


def main():
    raiz = Path(__file__).parent
    out = raiz / "svg"
    out.mkdir(exist_ok=True)
    g = geometria()

    for tema in TEMAS:
        escribir(out / f"logo-{tema}.svg", svg(g, pinturas_tema(tema)))

    # Adaptable: sigue el modo claro/oscuro del sistema (también dentro de <img>)
    clases = {"grilla": 'class="grilla"', "punto": 'class="punto"', "trazo": "url(#trazo)", "letra": "url(#letra)",
              **{f"{rol}{i}": f'class="{rol}{i}"' for rol in ("trazo", "letra") for i in (0, 1)}}
    estilo = css("claro") + "@media (prefers-color-scheme:dark){" + css("oscuro") + "}"
    escribir(out / "logo.svg", svg(g, clases, estilo))

    # Monocromo: todo en currentColor (toma el color del texto donde se inserte)
    mono = {"grilla": 'stroke="currentColor"', "punto": 'fill="currentColor"',
            "trazo": "currentColor", "letra": "currentColor"}
    escribir(out / "logo-mono.svg", svg(g, mono, raiz=f' color="{ESCALA[400]}"'))

    try:
        import resvg_py
    except ImportError:
        print("resvg_py no instalado: se omiten los PNG")
    else:
        png = raiz / "png"
        png.mkdir(exist_ok=True)
        for tema in TEMAS:
            for w in (512, 1024, 2048):
                data = resvg_py.svg_to_bytes(svg_path=str(out / f"logo-{tema}.svg"),
                                             width=w, height=round(w * H / W))
                (png / f"logo-{tema}-{w}.png").write_bytes(bytes(data))
        # Avatar cuadrado para redes: logo oscuro centrado, entra entero en un recorte circular
        lado, ancho = 1024, 1024 * AVATAR_ANCHO
        alto = ancho * H / W
        caja = f' x="{f((lado - ancho) / 2)}" y="{f((lado - alto) / 2)}" width="{f(ancho)}" height="{f(alto)}"'
        avatar = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {lado} {lado}">'
                  f'<rect width="{lado}" height="{lado}" fill="{FONDO_AVATAR}"/>'
                  f'{svg(g, pinturas_tema("oscuro"), raiz=caja)}</svg>')
        data = resvg_py.svg_to_bytes(svg_string=avatar, width=lado, height=lado)
        (png / f"avatar-{lado}.png").write_bytes(bytes(data))
    print("Logo generado en", out)


if __name__ == "__main__":
    main()
