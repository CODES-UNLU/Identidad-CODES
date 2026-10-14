# Logo CODES++

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="svg/logo-oscuro.svg">
  <img src="svg/logo-claro.svg" alt="Logo CODES++" width="320">
</picture>

Logo vectorizado del Centro Organizado de Estudiantes de Sistemas (UNLu): un globo
terráqueo que emerge de un libro abierto, con la **C** al frente.

La paleta es una única familia teal construida alrededor del color principal de
[codesunlu.tech](https://www.codesunlu.tech/) (`#39c0c3`).

## Archivos

| Archivo | Uso |
|---|---|
| `svg/logo.svg` | Adaptable: cambia de colores según el modo claro/oscuro del sistema. Sirve también como favicon |
| `svg/logo-claro.svg` | Para fondos claros |
| `svg/logo-oscuro.svg` | Para fondos oscuros, como el `#0f0f0f` del sitio |
| `svg/logo-mono.svg` | Un solo color (`currentColor`, por defecto `#39c0c3`) |
| `png/logo-claro-*.png`, `png/logo-oscuro-*.png` | Exportaciones a 512, 1024 y 2048 px con fondo transparente |
| `png/avatar-1024.png` | Avatar cuadrado para redes sobre `#0f0f0f`; también entra en recortes circulares |
| `vista-previa.html` | Versiones, fondos del sitio, tamaños chicos y paleta |

## Paleta

Un solo tono (OKLCH h ≈ 197,6°) en pasos parejos de luminosidad. Los escalones
300, 400 y 600 son exactamente los colores del sitio.

| Escalón | Color | En el sitio |
|---|---|---|
| 50 | `#e7fafa` | |
| 100 | `#c8f3f4` | |
| 200 | `#95e7e8` | |
| 300 | `#5dd5d8` | `--primary-light` |
| 400 | `#39c0c3` | `--primary` |
| 500 | `#30a5a8` | |
| 600 | `#2a8a8d` | `--primary-dark` |
| 700 | `#1d6d6f` | |
| 800 | `#125355` | |
| 900 | `#083b3c` | |
| 950 | `#022324` | |

### Colores del logo

En fondo claro, lo más importante es lo más profundo; en fondo oscuro, lo más
luminoso. Los degradados van a 135°, como los del sitio.

| Elemento | Fondo claro | Fondo oscuro |
|---|---|---|
| Grilla del globo | 300 | 700 |
| Contorno y libro | 400 → 600 | 300 → 500 |
| Letra C | 500 → 700 | 200 → 400 |

## Uso

```html
<!-- Se adapta solo al tema claro/oscuro -->
<img src="svg/logo.svg" alt="CODES++" width="160">

<!-- Favicon -->
<link rel="icon" href="svg/logo.svg" type="image/svg+xml">
```

Para el monocromo, insertar `logo-mono.svg` en línea y definir `color` por CSS
(por ejemplo `#fff` sobre fotos o `#1a1a1a` en impresiones de un color).

## Regenerar

Los colores y la geometría están al principio de `generar_logo.py` (`ESCALA`, `TEMAS`
y el bloque de geometría).

```sh
pip install resvg_py   # opcional, para exportar los PNG
python generar_logo.py
```
