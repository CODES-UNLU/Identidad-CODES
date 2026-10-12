# 🎨 Paleta de Colores Oficial de CODES++

> **Documento de especificación y tokens de diseño extraídos del sitio web oficial:**  
> 🌐 [https://www.codesunlu.tech/](https://www.codesunlu.tech/)  
> 🏛️ **Centro Organizado de Estudiantes de Sistemas (CODES++) - Universidad Nacional de Luján (UNLu)**  
> 📅 *Extracción y análisis: Octubre 2026*

---

## 📌 1. Identidad Visual y Filosofía de Diseño

El diseño de la plataforma web de **CODES++** se basa en una estética **Dark-first moderna e industrial de alta tecnología**, orientada a estudiantes y profesionales del desarrollo de software.

- **Color Insignia (Brand Accent):** Turquesa / Cyan eléctrico (`#39c0c3`), que evoca conectividad, dinamismo, código y frescura.
- **Atmósfera:** Fondos oscuros de contraste profundo (`#0f0f0f` a `#2d2d2d`) que reducen la fatiga visual.
- **Acabados:** Uso de *Glassmorphism* (fondos translúcidos con `backdrop-filter: blur()`), degradados lineales en ángulo de 135° y bordes con sutiles halos de resplandor (*cyan glow*).
- **Meta Tags de Aplicación / PWA:**
  - `theme-color`: `#39c0c3`
  - `msapplication-TileColor`: `#39c0c3`

---

## 💎 2. Colores Principales de Marca (Brand Core)

Estos son los valores fundamentales declarados en `:root` que definen toda la identidad gráfica:

| Token / Variable CSS | Color Hex | RGB | HSL | Rol en la Interfaz / Marca |
| :--- | :---: | :---: | :---: | :--- |
| `--primary` | `#39c0c3` | `rgb(57, 192, 195)` | `hsl(181, 55%, 49%)` | **Color Identitario Primario**. Botones principales, enlaces activos, acentos y logotipo. |
| `--primary-dark` | `#2a8a8d` | `rgb(42, 138, 141)` | `hsl(182, 54%, 36%)` | **Tono Oscuro / Hover**. Extremo inferior de degradados institucionales y hover de botones. |
| `--primary-light` | `#5dd5d8` | `rgb(93, 213, 216)` | `hsl(181, 62%, 61%)` | **Tono Claro / Resaltado**. Extremo superior de degradados luminosos, destellos y acentos vivos. |
| `--secondary` | `#1a1a1a` | `rgb(26, 26, 26)` | `hsl(0, 0%, 10%)` | **Secundario Neutro**. Barra de navegación, pie de página (*footer*) y contenedores secundarios. |
| `--accent` | `#39c0c3` | `rgb(57, 192, 195)` | `hsl(181, 55%, 49%)` | Alias funcional de acento principal. |
| `--accent-light` | `#5dd5d8` | `rgb(93, 213, 216)` | `hsl(181, 62%, 61%)` | Alias funcional para interacciones y brillos. |
| `--accent-hover` | `#2a8a8d` | `rgb(42, 138, 141)` | `hsl(182, 54%, 36%)` | Alias funcional para estados `:hover` y `:active`. |

---

## 🌌 3. Escala de Superficies y Fondos (Dark UI Hierarchy)

El sitio utiliza una jerarquía de elevación en escala de grises oscuros para separar capas y contenido:

| Nivel de Elevación | Variable CSS | Color Hex | RGB | Propósito / Uso |
| :--- | :--- | :---: | :---: | :--- |
| **Capa 0 (Base)** | `--background` | `#0f0f0f` | `rgb(15, 15, 15)` | Fondo global del `<body>` y contenedor raíz de la página. |
| **Capa 1 (Secciones)** | `--background-alt` | `#1a1a1a` | `rgb(26, 26, 26)` | Fondos de secciones alternas, headers y footer. |
| **Capa 2 (Tarjetas)** | `--background-card` | `#2d2d2d` | `rgb(45, 45, 45)` | Fondo de tarjetas (`.card`), modales y paneles interactivos. |
| **Capa 3 (Elevada)** | *(Superficie hover)* | `#3a3a3a` | `rgb(58, 58, 58)` | Superficies en elevación secundaria o estados hover. |
| **Especial (Charlas)** | *(Hero radial)* | `#1a1a2e` → `#16213e` | — | Fondo espacial azul nocturno para eventos y charlas técnicas. |

---

## 📝 4. Tipografía y Textos

La legibilidad se garantiza mediante cuatro niveles de contraste contra fondos oscuros:

| Variable CSS | Color Hex | RGB | Uso Recomendado |
| :--- | :---: | :---: | :--- |
| `--text` / `--text-primary` | `#ffffff` | `rgb(255, 255, 255)` | Títulos principales (`h1`, `h2`), texto de botones activos, texto de alto impacto. |
| `--text-secondary` | `#e0e0e0` | `rgb(224, 224, 224)` | Párrafos de lectura, subtítulos principales. |
| `--text-light` | `#b0b0b0` | `rgb(176, 176, 176)` | Textos descriptivos de tarjetas, etiquetas secundarias. |
| `--text-muted` | `#6c757d` | `rgb(108, 117, 125)` | Fechas, metadatos, texto de pie de foto y deshabilitados. |

---

## 🔲 5. Bordes y Divisores

| Variable CSS | Color Hex / Valor | RGB / Alpha | Función |
| :--- | :---: | :---: | :--- |
| `--border` | `#404040` | `rgb(64, 64, 64)` | Bordes normales de tarjetas, inputs y separadores visibles. |
| `--border-light` | `#2d2d2d` | `rgb(45, 45, 45)` | Bordes sutiles para delimitar zonas sin competir con el contenido. |
| *(Borde activo)* | `#39c0c3` | `rgb(57, 192, 195)` | Borde de tarjetas en estado `:hover` o campos de formulario `:focus`. |
| `--glass-border` | `rgba(255, 255, 255, 0.10)` | — | Borde translúcido para tarjetas de cristal (*glass effect*). |

---

## 🚦 6. Colores Semánticos y de Estado (Feedback)

| Estado | Variable CSS | Color Hex | Uso en la Web |
| :--- | :--- | :---: | :--- |
| **Éxito (Success)** | `--success` | `#51cf66` | Inscripciones abiertas, confirmaciones, estado "en vivo". |
| **Éxito Secundario** | *(Bootstrap)* | `#28a745` | Badges de estado positivo y links completados. |
| **Advertencia (Warning)** | `--warning` | `#ffd43b` | Próximos eventos, cupos limitados, alertas. |
| **Peligro (Danger / Error)**| *(Bootstrap)* | `#dc3545` | Errores de validación, convocatorias cerradas. |
| **Informativo (Info)** | *(Bootstrap)* | `#0dcaf0` | Avisos generales y categorías de recursos. |

---

## 🌈 7. Degradados Oficiales (Gradients)

El ecosistema visual de CODES++ destaca por degradados limpios con ángulo de 135 grados:

### 🌟 Gradientes Institucionales (Firma CODES)

```css
/* Gradiente insignia: Botones principales, títulos degradados, badges y acentos */
--gradient: linear-gradient(135deg, #39c0c3 0%, #2a8a8d 100%);

/* Gradiente claro: Resaltados vivos, hovers luminosos */
--gradient-light: linear-gradient(135deg, #5dd5d8 0%, #39c0c3 100%);

/* Gradiente de acento alternativo */
--gradient-accent: linear-gradient(135deg, #39c0c3 0%, #5dd5d8 100%);
```

### 🚀 Gradientes de Secciones Especiales (Charlas & Tech)

```css
/* Cyan Neón a Azul Eléctrico */
--primary-gradient: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);

/* Verde Neón a Menta Aqua */
--secondary-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);

/* Rosa Neón a Amarillo Sol */
--accent-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
```

### 🧩 Gradientes Temáticos para Tarjetas (Valores & Recursos)

Cada tarjeta temática del sitio utiliza un degradado identificatorio en sus iconos:

1. **Pasión & Comunidad:** `linear-gradient(135deg, #ff6b6b, #ff8e8e)` *(Coral a Rosa pastel)*
2. **Innovación & Tecnología:** `linear-gradient(135deg, #4ecdc4, #44a08d)` *(Turquesa a Verde azulado)*
3. **Aprendizaje Continuo:** `linear-gradient(135deg, #45b7d1, #96c93d)` *(Celeste a Verde lima)*
4. **Colaboración:** `linear-gradient(135deg, #f093fb, #f5576c)` *(Lila a Fucsia)*
5. **Excelencia:** `linear-gradient(135deg, #4facfe, #00f2fe)` *(Azul a Cian)*
6. **Futuro:** `linear-gradient(135deg, #43e97b, #38f9d7)` *(Verde esmeralda a Menta)*

---

## 🔮 8. Glassmorphism, Sombras y Efectos Glow

### Variables de Cristal (Glassmorphism)
```css
--glass-bg: rgba(255, 255, 255, 0.05);
--glass-border: rgba(255, 255, 255, 0.10);
--glass-highlight: rgba(255, 255, 255, 0.20);
```

### Sombras y Elevaciones
```css
--shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
--shadow-hover: 0 8px 30px rgba(0, 0, 0, 0.4);
--shadow-card: 0 2px 15px rgba(0, 0, 0, 0.2);
```

### Halos de Resplandor (Cyan Glow)
Utilizados en hovers de tarjetas e iconos interactivos:
```css
/* Resplandor característico del botón y tarjeta de CODES */
box-shadow: 0 8px 25px rgba(57, 192, 195, 0.30); /* #39c0c34d */

/* Anillo de foco accesible */
outline: 3px solid rgba(57, 192, 195, 0.50);     /* #39c0c380 */
```

---

## 🧪 9. Escala de Transparencias del Color Insignia (`#39c0c3`)

En las hojas de estilo del sitio se utiliza intensivamente el canal Alfa del color insignia:

| Notación Hex (8-dígitos) | Equivalente RGBA | Opacidad | Uso en el Sitio |
| :---: | :---: | :---: | :--- |
| `#39c0c308` | `rgba(57, 192, 195, 0.03)` | 3% | Gradientes de fondo muy sutiles |
| `#39c0c30d` | `rgba(57, 192, 195, 0.05)` | 5% | Capas de superposición base en tarjetas |
| `#39c0c31a` | `rgba(57, 192, 195, 0.10)` | 10% | Hover suave en items de lista y calendarios |
| `#39c0c326` | `rgba(57, 192, 195, 0.15)` | 15% | Fondos de tags y chips |
| `#39c0c333` | `rgba(57, 192, 195, 0.20)` | 20% | Bordes activos sutiles |
| `#39c0c34d` | `rgba(57, 192, 195, 0.30)` | 30% | Sombras proyectadas con resplandor (*cyan glow*) |
| `#39c0c366` | `rgba(57, 192, 195, 0.40)` | 40% | Flechas, indicadores y divisores resaltados |
| `#39c0c380` | `rgba(57, 192, 195, 0.50)` | 50% | Anillos de selección (`:focus-visible`) |
| `#39c0c3cc` | `rgba(57, 192, 195, 0.80)` | 80% | Acentos translúcidos de alto contraste |

---

## 🎨 10. Guía de Aplicación para el Logotipo de CODES++

Al vectorizar o componer el imagotipo (globo terráqueo con paralelos, meridianos y la letra **C**):

1. **Versión para Fondos Oscuros (Sitio Web Oficial - `#0f0f0f`):**
   - **Contorno y Globo:** Emplear la transición de `--primary-light` (`#5dd5d8`) hacia `--primary` (`#39c0c3`).
   - **La 'C' Institucional:** Debe destacar como elemento focal, iniciando en un tono menta luminoso (`#7cf5d6` / `#5ef2c8`) y cerrando en el cian oficial (`#39c0c3`).
   - **Meridianos / Red de Fondo:** Tonos cian profundos (`#1a5f61` / `#25808b`) para no competir con el trazo principal.
2. **Versión para Fondos Claros / Papelería:**
   - Incrementar la densidad cromática utilizando `--primary-dark` (`#2a8a8d`) y azules profundos (`#1f6fa6`, `#0e4a5a`) para preservar el contraste según WCAG AA.
3. **Versión Monocromática:**
   - Para fondos oscuros: `#ffffff` o `#39c0c3`.
   - Para fondos claros: `#1a1a1a` o `#2a8a8d`.

---

## 💻 11. Snippets de Integración Directa

### CSS Nativo (`theme.css`)
```css
:root {
  /* Brand */
  --codes-primary: #39c0c3;
  --codes-primary-dark: #2a8a8d;
  --codes-primary-light: #5dd5d8;
  --codes-secondary: #1a1a1a;

  /* Surfaces */
  --codes-bg-base: #0f0f0f;
  --codes-bg-alt: #1a1a1a;
  --codes-bg-card: #2d2d2d;

  /* Typography */
  --codes-text-primary: #ffffff;
  --codes-text-secondary: #e0e0e0;
  --codes-text-light: #b0b0b0;
  --codes-text-muted: #6c757d;

  /* Borders & Shadows */
  --codes-border: #404040;
  --codes-border-light: #2d2d2d;
  --codes-glow: 0 8px 25px rgba(57, 192, 195, 0.3);

  /* Gradients */
  --codes-gradient: linear-gradient(135deg, #39c0c3 0%, #2a8a8d 100%);
  --codes-gradient-light: linear-gradient(135deg, #5dd5d8 0%, #39c0c3 100%);
}
```

### Configuración para Tailwind CSS (`tailwind.config.js`)
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        codes: {
          primary: {
            DEFAULT: '#39c0c3',
            dark: '#2a8a8d',
            light: '#5dd5d8',
          },
          dark: {
            base: '#0f0f0f',
            alt: '#1a1a1a',
            card: '#2d2d2d',
            elevated: '#3a3a3a',
          },
          border: {
            DEFAULT: '#404040',
            light: '#2d2d2d',
          },
          text: {
            primary: '#ffffff',
            secondary: '#e0e0e0',
            light: '#b0b0b0',
            muted: '#6c757d',
          }
        }
      },
      backgroundImage: {
        'codes-gradient': 'linear-gradient(135deg, #39c0c3 0%, #2a8a8d 100%)',
        'codes-gradient-light': 'linear-gradient(135deg, #5dd5d8 0%, #39c0c3 100%)',
      },
      boxShadow: {
        'codes-glow': '0 8px 25px rgba(57, 192, 195, 0.3)',
      }
    }
  }
}
```

### Tokens en Formato JSON (`codes-palette.json`)
```json
{
  "name": "CODES++ Official Web Palette",
  "source": "https://www.codesunlu.tech/",
  "colors": {
    "primary": "#39c0c3",
    "primaryDark": "#2a8a8d",
    "primaryLight": "#5dd5d8",
    "secondary": "#1a1a1a",
    "background": "#0f0f0f",
    "backgroundAlt": "#1a1a1a",
    "backgroundCard": "#2d2d2d",
    "text": "#ffffff",
    "textSecondary": "#e0e0e0",
    "textLight": "#b0b0b0",
    "textMuted": "#6c757d",
    "border": "#404040",
    "borderLight": "#2d2d2d",
    "success": "#51cf66",
    "warning": "#ffd43b"
  }
}
```
