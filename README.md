# Logo CODES++

Logo vectorizado del Centro Organizado de Estudiantes de Sistemas, con una paleta
análoga construida alrededor del color principal de [codesunlu.tech](https://www.codesunlu.tech/) (`#39c0c3`).

## Archivos

| Archivo | Uso |
|---|---|
| `svg/logo.svg` | Adaptable: cambia de colores según el modo claro/oscuro del sistema |
| `svg/logo-claro.svg` | Para fondos claros |
| `svg/logo-oscuro.svg` | Para fondos oscuros |
| `svg/logo-mono.svg` | Un solo color (`currentColor`) |
| `png/` | Exportaciones a 512, 1024 y 2048 px |
| `vista-previa.html` | Paleta y logo en ambos modos |

## Paleta

| Nombre | Color |
|---|---|
| Menta | `#4fe3c1` |
| Teal (principal) | `#39c0c3` |
| Océano | `#2a8fd0` |
| Profundo | `#0e4a5a` |
| Abismo | `#12385e` |

## Regenerar

Los colores y la geometría están en `generar_logo.py` (bloque `TEMAS`).

```sh
pip install resvg_py   # opcional, para exportar los PNG
python generar_logo.py
```
